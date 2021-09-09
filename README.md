## 用途

如果你的群bot里装有setu_renew这款学习组件，每当你的群员检索其中内容时，本插件就会根据群员搜索的内容做记录，将来一段时间后，我们可以查询一下他的xp内容来了解他的学习状态。

## 使用方法

本插件只是插件，只能依附于setu_renew这款hoshinobot的学习组件。原理是在setu_renew这块模组里添加代码，然后修改一下setu_renew里的部分代码

**没有修改业务逻辑，仅做功能添加**

**1.备份原有的setu_renew模组**

2.下载本项目代码，直接将压缩包内的文件放入setu_renew文件夹里

3.如果你的Python没有wordcloud库，可以用pip install wordcloud安装，如果安装失败可以用项目里的离线包wordcloud-1.8.1-cp39-cp39-win_amd64.whl

4.迁移代码(复制粘贴)

4.1.1打开setu_renew的base.py，在import区粘贴以下代码

```python
from .xpRecorder import *
```

4.1.2打开setu_renew的base.py，找到search_setu()这个函数，修改它

需要修改函数的参数列表，以及在相应位置调用方法，具体如下

```python
async def search_setu(group_id,uid, keyword, num): # 为该函数新增uid参数
	insert_xp_keyword(uid,keyword)
  # 在此处粘贴该代码，用于记录keyword
	source_list = []
	if get_group_config(group_id, 'lolicon') and get_group_config(group_id, 'lolicon_r18'):
		source_list.append(2)
	elif get_group_config(group_id, 'lolicon'):
		source_list.append(0)
	elif get_group_config(group_id, 'lolicon_r18'):
		source_list.append(1)
	if get_group_config(group_id, 'acggov'):
		source_list.append(3)
	
	if len(source_list) == 0:
		return []
	
	image_list = None
	msg_list = []
	while len(source_list) > 0 and len(msg_list) == 0:
		source = source_list.pop(random.randint(0, len(source_list) - 1))
		if source == 0:
			image_list = await lolicon_search_setu(keyword, 0, num)
		elif source == 1:
			image_list = await lolicon_search_setu(keyword, 1, num)
		elif source == 2:
			image_list = await lolicon_search_setu(keyword, 2, num)
		elif source == 3:
			image_list = await acggov_search_setu(keyword, num)
		if image_list and len(image_list) > 0:
			for image in image_list:
				insert_xp(uid,image['tags'])
  # 在此处粘贴代码，记录xp的tag
				msg_list.append(format_setu_msg(image))
	return msg_list


```

4.2.1打开setu_renew的lolicon.py，找到get_setu_native()这个函数，修改它，如下

```python
def get_setu_native(r18=0, uid=0):
	image = generate_image_struct()
	
	path = f'setu_mix/lolicon'
	if r18 == 1:
		path = f'setu_mix/lolicon_r18'
	elif r18 == 2:
		if random.randint(1, 100) > 50:
			path = f'setu_mix/lolicon_r18'
	res = R.img(path)
	if not os.path.exists(res.path):
		return image
	
	if uid == 0:
		fn = random.choice(os.listdir(res.path))
		if fn.split('.')[0].isdigit():
			uid = int(fn.split('.')[0])
	
	if not uid:
		return image
	
	image['id'] = int(uid)
	image['native'] = True
	
	path += f'/{uid}'
	res = R.img(path)
	try:
		image['data'] = res.path + '.jpg'
		with open(res.path + '.json', encoding='utf8') as f:
			d = json.load(f)
			if 'title' in d:
				image['title'] = d['title']
			if 'author' in d:
				image['author'] = d['author']
			if 'url' in d:
				image['url'] = d['url']
			if 'tags' in d:
                   # 新增这两行
				image['tags'] = d['tags']
     # 新增这两行
	except:
		pass
	
	return image

```

4.3.1打开setu_renew的__init__.py，在import区导入

```python
from .xpcloud import *
from hoshino.typing import MessageSegment
PATH = os.path.dirname(__file__)

```

4.3.2打开setu_renew的__init__.py，寻找await search_setu，添加参数

```python
await search_setu(gid, keyword, num)
# 改为
await search_setu(gid,uid, keyword, num)

```

4.3.3打开setu_renew的__init__.py，拉到最底下，粘贴以下内容

```python
@sv.on_prefix('看他xp')
async def wtf_his_xp(bot,ev):
    for i in ev.message:
        if i.type == 'at' and i.data['qq'] != 'all':
            uid = i.data['qq']
    try:
        print_word_to_img(uid)
        msg = "此人最常搜TOP10:\n"+MessageSegment.image("file:///" + PATH + "/output_keyword.png")+"最常用标签TOP10:\n"+MessageSegment.image("file:///" + PATH + "/output_tag.png")
        await bot.send(ev, msg, at_sender=True)
        return
    except:
        traceback.print_exc()
        await bot.send(ev, '出错了！！', at_sender=True)
        return


@sv.on_fullmatch('我的xp')
async def wtf_my_xp(bot,ev):
    uid = ev.uid
    try:
        print_word_to_img(uid)
        msg = "最常搜TOP10:\n" + MessageSegment.image(
            "file:///" + PATH + "/output_keyword.png") + "最常用标签TOP10:\n" + MessageSegment.image(
            "file:///" + PATH + "/output_tag.png")
        await bot.send(ev, msg, at_sender=True)
        return
    except:
        traceback.print_exc()
        await bot.send(ev, '出错了！！', at_sender=True)
        return
```

重启机器人，发送 看他xp@某人看他的xp记录，或者发送 我的xp 看自己的xp

