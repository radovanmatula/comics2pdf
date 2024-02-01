import os
import shutil
import zipfile
import patoolib
from fpdf import FPDF

###

def create_cbz(source, filename=None):
    """
    `source` can either be a single directory of `.jpg` files or a list of dictioanries
    `filename` ... what should the `.cbz` file be named
    """
    
    if filename is not None:
        file = filename + '.cbz'
    else:
        file = os.path.basename(source) + '_(c2p).cbz'

    start_dir = os.getcwd()
    # create a temporary directory
    temp_dir = os.path.join(os.getcwd(),'temp_c2p/')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)

    os.mkdir(temp_dir)

    #copy images into a temporary directory
    if isinstance(source, list):
        for i,directory in enumerate(source):
            list_of_imgs = os.listdir(directory)
            list_of_imgs.sort()

            for j,img in enumerate(list_of_imgs):
                old_img_path = directory + img
                temp_img_path = temp_dir + img
                img_no = f'img_'
                if i<10:
                    img_no += f'0{i}_'
                else:
                    img_no += f'{i}_'
                if j<10:
                    img_no += f'0{j}'
                else:
                    img_no += f'{j}'
                
                img_no += '.jpg'
                new_img_path = temp_dir + img_no

                shutil.copy(old_img_path, temp_dir)
                os.rename(temp_img_path, new_img_path)

    else:
        list_of_imgs = os.listdir(source)
        list_of_imgs.sort()

        for j,img in enumerate(list_of_imgs):
            old_img_path = d + img
            temp_img_path = temp_dir + img
            img_no = f'img_'
            if i<10:
                img_no += f'0{i}_'
            else:
                img_no += f'{i}_'
            if j<10:
                img_no += f'0{j}'
            else:
                img_no += f'{j}'

            img_no += '.jpg'
            new_img_path = temp_dir + img_no

            shutil.copy(old_img_path, temp_dir)
            os.rename(temp_img_path, new_img_path)

    temp_list_of_imgs = os.listdir(temp_dir)
    temp_list_of_imgs.sort()
    
    os.chdir(temp_dir)
    with zipfile.ZipFile(file, 'w') as cbz:
        for img in temp_list_of_imgs:
            cbz.write(img)

    shutil.copy(file, start_dir)
    os.chdir(start_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)


def create_pdf(source, filename=None):
   
    """
    source can be either a directory/list of directories of `.jpg` files, or a `.cbz` file, or a `.cbr` file
    `filename` ... what should the `.cbz` file be named
    """

    if filename is not None:
        file = filename + '.pdf'
    else:
        file = os.source.basename(source) + '_(c2p).pdf'

    # create a temporary directory
    temp_dir = os.path.join(os.getcwd(),'temp_c2p/')

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)
    os.mkdir(temp_dir)

    if os.path.isdir(source) or isinstance(source, list): 
        create_cbz(source=source, filename=filename)
        cbz_path = os.path.join(os.getcwd(), f'{filename}.cbz')
        with zipfile.ZipFile(cbz_path, 'r') as zip_file:
            zip_file.extractall(temp_dir)

    elif source[-4:] == '.cbz':
        cbz_path = source
        with zipfile.ZipFile(cbz_path, 'r') as zip_file:
            zip_file.extractall(temp_dir)

    elif source[-4:] == '.cbr':
        cbr_path = source
        patoolib.extract_archive(archive=cbr_path, outdir=temp_dir)

    else:
        print("We do not support this format as of now.")

    temp_list_of_imgs = os.listdir(temp_dir)
    temp_list_of_imgs.sort()

    pdf = FPDF()
    for img in temp_list_of_imgs:
        img_path = os.path.join(temp_dir, img)
        pdf.add_page()
        pdf.image(img_path, x=10, y=8, w=190)

    pdf.output(file)

    shutil.rmtree(temp_dir, ignore_errors=True)



