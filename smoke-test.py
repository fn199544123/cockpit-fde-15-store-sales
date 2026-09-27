#!/usr/bin/env python3
"""在宿主机运行 python3 smoke-test.py；需要 Python Playwright 与 Chromium。"""
import csv, functools, io, json, threading
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from datetime import date, timedelta
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
class Handler(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
results=[]
def check(name,condition):
    if not condition: raise AssertionError(name)
    results.append({'name':name,'status':'passed'})
result={'title':'某企业 · 门店销售看板','entry':'index.html','identity':'douyin','features':['门店与品类销售记录新增、修改','日期、门店、品类联合筛选','按分计算销售额与品类占比','去年同期同比、上一等长区间环比','下降至少20%的门店红色预警','无可比基数显示暂无可比数据','localStorage 持久化','确认重置与筛选结果 CSV 导出','桌面与手机布局'], 'tests':results,'limitations':['演示数据仅当前浏览器保存，无后台、多人同步或真实实时采集。','销售记录不代表营业日完整覆盖；同比使用去年同日期区间，环比使用上一等长区间。','代码上传待补：未提供目标仓库与上传授权。','外部预览地址由素材中台接入；未对外发布。']}
try:
  with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
    context=browser.new_context(viewport={'width':1440,'height':1050},accept_downloads=True)
    page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(f'http://127.0.0.1:{server.server_port}/index.html')
    def amount(): return float(page.locator('#total').inner_text().replace(',',''))
    def select(id,value): page.locator('#'+id).select_option(value)
    def fill(id,value): page.locator('#'+id).fill(value);page.locator('#'+id).dispatch_event('change')
    today=date.today().isoformat()
    seed=page.evaluate("JSON.parse(localStorage.getItem('development-15-sales-v1'))")
    start=(date.today()-timedelta(days=6)).isoformat()
    expected=sum(r['cents'] for r in seed if start<=r['date']<=today)/100
    check('初始金额与原始销售记录求和一致',amount()==expected)
    check('二门店存在下降预警且标红',page.locator('#storesBody tr.alert-row').filter(has_text='二门店').count()==1)
    select('store','一门店');select('category','食品饮料');fill('start',today);fill('end',today)
    original=amount()
    page.click('#add');page.fill('#saleAmount','123.45');page.click('button:has-text("保存销售")')
    check('新增123.45元后金额实时增加且筛选联动',round(amount()-original,2)==123.45 and '2 笔' in page.locator('#listCount').inner_text())
    row=page.locator('#recordsBody tr').filter(has_text='123.45');row.get_by_role('button').click();page.fill('#saleAmount','223.45');page.click('button:has-text("保存销售")')
    check('修改销售后金额精确更新100元',round(amount()-original,2)==223.45)
    page.reload();select('store','一门店');select('category','食品饮料');fill('start',today);fill('end',today)
    check('刷新后持久化记录及汇总正确',round(amount()-original,2)==223.45)
    select('store','三门店');check('门店筛选排除其他门店新记录','223.45' not in page.locator('#recordsBody').inner_text())
    select('store','一门店');select('category','日用百货');check('品类筛选排除其他品类记录','223.45' not in page.locator('#recordsBody').inner_text())
    select('category','食品饮料')
    with page.expect_download() as download: page.click('#export')
    content=Path(download.value.path()).read_text(encoding='utf-8-sig');out=list(csv.reader(io.StringIO(content)))
    check('CSV导出当前筛选全部记录且金额一致',len(out)==3 and all(r[2]=='一门店' and r[3]=='食品饮料' for r in out[1:]) and round(sum(float(r[4]) for r in out[1:]),2)==amount())
    # 新日期创建无基数场景，保存时当前筛选仍为空。
    fill('start','2040-01-10');fill('end','2040-01-10')
    check('空状态与无基数处理',amount()==0 and page.locator('#yoy').inner_text()=='暂无可比数据' and page.locator('#mom').inner_text()=='暂无可比数据')
    page.click('#add');page.fill('#saleDate','2040-01-10');page.fill('#saleAmount','50');page.click('button:has-text("保存销售")')
    check('有销售但无同期基数不伪造增长率',amount()==50 and page.locator('#yoy').inner_text()=='暂无可比数据' and page.locator('#mom').inner_text()=='暂无可比数据')
    page.click('#add');page.fill('#saleDate','2040-01-09');page.fill('#saleAmount','100');page.click('button:has-text("保存销售")')
    check('等长区间环比计算与红色预警',page.locator('#mom').inner_text()=='-50.00%' and page.locator('#storesBody .warn').count()==1 and amount()==50)
    page.click('#add');page.fill('#saleDate','2039-01-10');page.fill('#saleAmount','200');page.click('button:has-text("保存销售")')
    check('去年同期同比精确计算',page.locator('#yoy').inner_text()=='-75.00%')
    before=page.evaluate("JSON.parse(localStorage.getItem('development-15-sales-v1')).length")
    page.click('#add');page.fill('#saleAmount','-1');page.click('button:has-text("保存销售")')
    check('拒绝负数金额',page.locator('#editor').is_visible() and page.evaluate("JSON.parse(localStorage.getItem('development-15-sales-v1')).length")==before);page.click('#cancel')
    fill('start','2040-01-11');check('倒置日期阻止统计和导出',bool(page.locator('#filterError').inner_text()) and page.locator('#export').is_disabled())
    page.click('#defaultFilter');page.click('#reset');page.click('#cancelReset')
    check('取消重置保留数据',page.evaluate("JSON.parse(localStorage.getItem('development-15-sales-v1')).length")==before)
    page.click('#reset');page.click('#confirmReset');check('确认重置恢复种子数据',page.evaluate("JSON.parse(localStorage.getItem('development-15-sales-v1'))")==seed)
    # 特殊基数为零与闰日比较直接验证统计函数，不向存储注入无效记录。
    check('零基数不产生Infinity或伪造比例',page.evaluate('rate([{cents:100}],[{cents:0}])') is None)
    check('闰日映射上一年2月28日',page.evaluate("lastYear('2024-02-29')")=='2023-02-28')
    check('键名前缀隔离',page.evaluate("Object.keys(localStorage).every(k=>k.startsWith('development-15-'))"))
    page.screenshot(path=str(ROOT/'evidence-desktop.png'),full_page=True)
    page.set_viewport_size({'width':390,'height':844})
    check('手机布局无页面横向溢出',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    page.click('#add');page.fill('#saleAmount','12.34');page.click('button:has-text("保存销售")')
    check('手机可以新增销售',not page.locator('#editor').is_visible())
    page.screenshot(path=str(ROOT/'evidence-mobile.png'),full_page=True)
    check('浏览器无JavaScript错误',not errors)
    # 模拟存储失败，保证不能误报已保存。
    page.evaluate("() => { Storage.prototype.setItem=function(){throw new Error('quota')}; }")
    page.click('#add');page.fill('#saleAmount','10');page.click('button:has-text("保存销售")')
    check('存储失败显示错误且不关闭编辑框',page.locator('#editor').is_visible() and '保存失败' in page.locator('#saveError').inner_text())
    browser.close()
  result['test_status']='passed';result['test_environment']='宿主机 / Python Playwright / headless Chromium';result['evidence']=['evidence-desktop.png','evidence-mobile.png']
except Exception as e:
  result['test_status']='failed';results.append({'name':'执行中断','status':'failed','detail':str(e)});raise
finally:
  server.shutdown();(ROOT/'development-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
  print(json.dumps(result,ensure_ascii=False,indent=2))
