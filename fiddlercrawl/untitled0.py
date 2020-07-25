from wechatarticles import ArticlesAPI
from wechatarticles import ArticlesUrls
from wechatarticles import Reader


username = "1078801674@qq.com"
password = "e07880e674"
nickname = "牛娃成长记"
query = ''
official_cookie = 'pgv_pvid=2211394424; pgv_pvi=7482549248; RK=B9wIEduYEP; ptcz=1e88b692f026a0380cd7bdbe7d880e9e0990085b54eabaa85de005c9ca23350f; o_cookie=1078801674; pac_uid=1_1078801674; ied_qq=o1078801674; tvfe_boss_uuid=938cbf1d9cf13793; ptui_loginuin=1078801674; pgv_si=s6930927616; uin=o1078801674; pt_sms_phone=136******74; pgv_info=ssid=s3177911849; rewardsn=; wxtokenkey=777; ua_id=AUmi575LwcR8XjekAAAAAIbZMBnOah5h7_z2NjPpK50=; xid=; openid2ticket_ooxNm0ckd-JZWIEn9WXJFrZDXDGU=; mm_lang=zh_CN; cert=UyyxUKsi1RLHXNQfcRvlWDGzrHKyhwn0; sig=h0112a244a354e2d414b254aedeba9c791a43ebc72f88a354307aa1017812d96a88c97631a1860e4368; skey=@Txm1DyqO9; master_key=OnHmdwIqkgCPz/bPN/H0kaPulEIa+utE9VNQC1zoPX8=; iip=0; pt2gguin=o1078801674; uuid=957a6b398961ec1c82cd9730d0ffd174; bizuin=3098758740; ticket=1b8259f084169fea80abcf0c1d91e4de7290ba10; ticket_id=gh_092b6a7a5014; noticeLoginFlag=1; rand_info=CAESIKgjOhmp3tqZQ5M3CTn+LJnfI5AOVx3O3RhD5WFjAdCy; slave_bizuin=3098758740; data_bizuin=3098758740; data_ticket=5ykkl7bxa3srJ+vPwm1WW5zU6F9M288NDVAoISwhyd17NyAuWA+e77gDK3E8LNI4; slave_sid=OTBpRV9BMXBLYXRpWmM3Vkx6Qnk1eHk0dWNWamx1d0E5eGU2WGF5RndqX3RxY0YxX3VabFk3alhjdlNMN0JPZWNqVjNCUWR6Z3JxMk9nVm5raEo3QlZ1dlB2a3hmREZzQ3A4ZGUyVFczbVJ1WDhiYUdDWExCakVJQW5IMG9LUUsxQUs3S2o5Nng5QW5WbEdo; slave_user=gh_092b6a7a5014; openid2ticket_oVE6zuGkDiPg1j-wfy86QI2MxUwY=jp6u5NMAsMFKhezo7oEs5RckXK0MhcszoXkljURsYmw='
token = '1889582131'

# 实例化爬取对象
# 账号密码自动获取cookie和token
test = ArticlesUrls(username=username, password=password)
# 手动输入账号密码
test = ArticlesUrls(cookie=official_cookie, token=token)

# 输入公众号名称，获取公众号文章总数
articles_sum = test.articles_nums(nickname)
# 输入公众号名称，获取公众号部分文章信息, 每次最大返回数为5个
articles_data = test.articles(nickname, begin="0", count="5")
# 输入公众号名称，获取公众号的一些信息
officical_info = test.official_info(nickname)
# 输入公众号名称，输入关键词，获取公众号相关文章信息, 每次最大返回数为5个
articles_data_query = test.articles(nickname, query=query, begin="0", count="5")
# 输入公众号名称，输入关键词，获取公众号相关文章总数
articles_sum_query = test.articles_nums(nickname, query=query)

# 支持自动获取appmsg_token和cookie
appmsg_token, cookie = Reader().contral(outfile)

# 实例化爬取对象
# 账号密码自动获取cookie和token
test = ArticlesInfo(appmsg_token=appmsg_token, cookie=wechat_cookie)
# 获取文章所有的评论信息(无需appmsg_token和cookie)
comments = test.comments(link)
# 获取文章阅读数在看点赞数
read_num, like_num, old_like_num = test.read_like_nums(link)