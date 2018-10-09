from PIL import Image
import os

def merge_label(label_path, label_pos, pic_path_list,pic_pos, save_path):
    label_pic = Image.open(label_path)
    label_size = label_pic.size
    fail_list = []
    for pic_path in pic_path_list:
        try:
            pic = Image.open(pic_path)
            if label_pos == 1:
                paste_pos = pic_pos
            if label_pos == 2:
                paste_pos = (pic_pos[0]-label_size[0],pic_pos[1])
            if label_pos == 3:
                paste_pos = (pic_pos[0],pic_pos[1]-label_size[1])
            if label_pos == 4:
                paste_pos = (pic_pos[0]-label_size[0],pic_pos[1]-label_size[1])
            pic.paste(label_pic,paste_pos)
            file_name = pic_path.split('/')[-1]
            pic.save(save_path+'/'+file_name)
        except:
            fail_list.append(pic_path)
            continue
    return True,fail_list

if __name__ == '__main__':
    merge_label('label.jpg',4, ['backpic.jpg'], (300,300),'image/')