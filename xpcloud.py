import wordcloud
from  .xpRecorder import *
ttf_path = os.path.abspath(os.path.join(SAVE_PATH,'SimHei.ttf'))
output_img_path_keyword = os.path.abspath(os.path.join(SAVE_PATH,'output_keyword.png'))
output_img_path_tag = os.path.abspath(os.path.join(SAVE_PATH,'output_tag.png'))

def print_word_to_img(qq):
    w = wordcloud.WordCloud(width=600,font_path=ttf_path,height=400)
    # keyword
    w.generate(get_xp_keyword(str(qq)))
    w.to_file(output_img_path_keyword)
    # tags
    w.generate(get_xp_tag(str(qq)))
    w.to_file(output_img_path_tag)