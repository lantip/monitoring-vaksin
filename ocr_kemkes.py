from PIL import Image, ImageOps, ImageEnhance
from pytesseract import image_to_string
import json
from os import walk
import os, re, dateparser

dir_path = os.path.dirname(os.path.realpath(__file__))

def sanitize(string):
    string = re.findall(r'\d+',string)
    return ''.join(string)

def extract(lines, idx):
    try:
        hsl = int(lines[idx].split()[len(lines[idx].split())-1].replace('.',''))
    except:
        hsl = lines[idx].split()[len(lines[idx].split())-1].replace('.','')
    return hsl
def ocr_date(jpg):
    
    im = Image.open(jpg)
    if '.png' in jpg:
        im = im.convert('RGB')    
    enhancer = ImageEnhance.Contrast(im)
    im_output = enhancer.enhance(5)
    img = im_output.convert('LA')
    data = image_to_string(img)
    result = {}
    lins = data.split('\n')
    lines = []
    for lin in lins:
        if len(lin.strip()) > 1:
            lines.append(lin)    

    im = Image.open(jpg)
    im = im.convert('LA')
    im = im.convert('RGB')
    im_invert = ImageOps.invert(im)
    enhancera = ImageEnhance.Contrast(im_invert)
    im_outputa = enhancera.enhance(3)
    #imga = im_outputa.convert('LA')
    #imga = im_invert.convert('LA')
    dataa = image_to_string(im_outputa)
    linsa = dataa.split('\n')
    linesa = []
    for lin in linsa:
        if len(lin.strip()) > 1:
            linesa.append(lin)   
    print([{k:v} for k,v in enumerate(lines)])
    print([{k:v} for k,v in enumerate(linesa)])
    issecond = False
    try:
        target = int(lines[2].replace('.',''))
        issecond = True
    except:
        target = None
    if not target:
        try:
            target =  int(lines[4].replace('.',''))
        except:
            target = None
    if target:
        if issecond:
            result['total_sasaran_vaksinasi'] = target
            result['sasaran_vaksinasi_sdmk'] = extract(lines,4)
            result['sasaran_vaksinasi_petugas_publik'] = extract(lines,6)
            result['sasaran_vaksinasi_lansia'] = extract(lines, 7)
            if linesa[11].lower() == 'vaksinasi':
                result['vaksinasi1'] = int(linesa[12].replace('.',''))
                result['vaksinasi2'] = int(linesa[14].replace('.',''))
            else:
                result['vaksinasi1'] = int(lines[11].split()[0].replace('.',''))
                result['vaksinasi2'] = int(lines[11].split()[1].replace('.',''))
            result['tahapan_vaksinasi'] = {}
            result['tahapan_vaksinasi']['sdm_kesehatan'] = {}
            if linesa[13] == 'Vaksinasi-2':
                result['tahapan_vaksinasi']['sdm_kesehatan']['total_vaksinasi1'] = int(sanitize(linesa[16].split()[1]))
                result['tahapan_vaksinasi']['sdm_kesehatan']['total_vaksinasi2'] = int(sanitize(linesa[16].split()[2]))
                result['tahapan_vaksinasi']['sdm_kesehatan']['sudah_vaksin1'] = int(linesa[17].split()[2].replace('.',''))
                result['tahapan_vaksinasi']['sdm_kesehatan']['sudah_vaksin2'] = int(linesa[17].split()[3].replace('.',''))
                result['tahapan_vaksinasi']['sdm_kesehatan']['tertunda_vaksin1'] = int(linesa[18].split()[1].replace('.',''))
                result['tahapan_vaksinasi']['sdm_kesehatan']['tertunda_vaksin2'] = int(linesa[18].split()[2].replace('.',''))
                result['tahapan_vaksinasi']['petugas_publik'] = {}
                result['tahapan_vaksinasi']['petugas_publik']['total_vaksinasi1'] = int(linesa[20].split()[1].replace('.',''))
                result['tahapan_vaksinasi']['petugas_publik']['total_vaksinasi2'] = int(linesa[20].split()[2].replace('.',''))
                result['tahapan_vaksinasi']['petugas_publik']['sudah_vaksin1'] = int(linesa[21].split()[2].replace('A','4').replace('T','7').replace('.',''))
                result['tahapan_vaksinasi']['petugas_publik']['sudah_vaksin2'] = int(linesa[21].split()[3].replace('.',''))
                #result['tahapan_vaksinasi']['petugas_publik']['tertunda_vaksin1'] = int(linesa[22].split()[1].replace('.',''))
                #result['tahapan_vaksinasi']['petugas_publik']['tertunda_vaksin2'] = int(linesa[22].split()[2].replace('.',''))
                result['tahapan_vaksinasi']['lansia'] = {}
                
                if 'Lansia' in linesa[25]:
                    if len(linesa[25].split()) > 2:
                        result['tahapan_vaksinasi']['lansia']['total_vaksinasi1'] = int(linesa[25].split()[1].replace('.',''))
                        result['tahapan_vaksinasi']['lansia']['total_vaksinasi2'] = int(linesa[25].split()[2].replace('.',''))
                else:
                    if len(linesa[23].split()) > 1:
                        result['tahapan_vaksinasi']['lansia']['total_vaksinasi1'] = int(linesa[23].split()[2].replace('.',''))
                    else:
                        result['tahapan_vaksinasi']['lansia']['total_vaksinasi1'] = int(linesa[23].split()[1].replace('.',''))
                    if len(linesa[23].split()) > 3:
                        result['tahapan_vaksinasi']['lansia']['total_vaksinasi2'] = int(linesa[23].split()[3].replace('.',''))
                    else:
                        result['tahapan_vaksinasi']['lansia']['total_vaksinasi2'] = 0
                    try:
                        result['tahapan_vaksinasi']['lansia']['sudah_vaksin1'] = int(linesa[24].split()[2].replace('.',''))
                    except:
                        pass
                    if len(linesa[24].split()) > 3:
                        result['tahapan_vaksinasi']['lansia']['sudah_vaksin2'] = int(linesa[24].split()[3].replace('.',''))
                    else:
                        result['tahapan_vaksinasi']['lansia']['sudah_vaksin2'] = 0
                #result['tahapan_vaksinasi']['lansia']['tertunda_vaksin1'] = int(linesa[22].split()[1].replace('.',''))
                #result['tahapan_vaksinasi']['lansia']['tertunda_vaksin2'] = int(linesa[22].split()[2].replace('.',''))
                result['cakupan'] = {}
                if lines[29] == 'Vaksinasi-1 Vaksinasi-2':
                    result['cakupan']['vaksinasi1'] = lines[30].split()[0]
                    result['cakupan']['vaksinasi2'] = lines[30].split()[1]
                    result['cakupan']['sdm_kesehatan_vaksinasi1'] = lines[32].split()[1]
                    result['cakupan']['sdm_kesehatan_vaksinasi2'] = lines[32].split()[2]
                    result['cakupan']['petugas_publik_vaksinasi1'] = lines[34].split()[2]
                    result['cakupan']['petugas_publik_vaksinasi2'] = lines[34].split()[3]

                else:
                    result['cakupan']['vaksinasi1'] = lines[29].split()[0]
                    result['cakupan']['vaksinasi2'] = lines[29].split()[1]
                    result['cakupan']['sdm_kesehatan_vaksinasi1'] = lines[31].split()[1]
                    result['cakupan']['sdm_kesehatan_vaksinasi2'] = lines[31].split()[2]
                    result['cakupan']['petugas_publik_vaksinasi1'] = lines[33].split()[1]
                    result['cakupan']['petugas_publik_vaksinasi2'] = lines[33].split()[2]
                #result['cakupan']['lansia_vaksinasi1'] = lines[31].split()[1]
                #result['cakupan']['lansia_vaksinasi2'] = lines[31].split()[2]
                result['date'] = dateparser.parse(lines[8]).strftime('%Y-%m-%d')
            else:
                result['tahapan_vaksinasi']['sdm_kesehatan']['total_vaksinasi1'] = int(linesa[13].split()[2].replace('.',''))
                result['tahapan_vaksinasi']['sdm_kesehatan']['total_vaksinasi2'] = int(linesa[13].split()[3].replace('.',''))
                result['tahapan_vaksinasi']['sdm_kesehatan']['sudah_vaksin1'] = int(linesa[14].split()[2].replace('.',''))
                result['tahapan_vaksinasi']['sdm_kesehatan']['sudah_vaksin2'] = int(linesa[14].split()[3].replace('.',''))
                result['tahapan_vaksinasi']['sdm_kesehatan']['tertunda_vaksin1'] = int(linesa[15].split()[1].replace('.',''))
                result['tahapan_vaksinasi']['sdm_kesehatan']['tertunda_vaksin2'] = int(linesa[15].split()[2].replace('.',''))
                result['tahapan_vaksinasi']['petugas_publik'] = {}
                result['tahapan_vaksinasi']['petugas_publik']['total_vaksinasi1'] = int(linesa[17].split()[2].replace('.',''))
                result['tahapan_vaksinasi']['petugas_publik']['total_vaksinasi2'] = int(linesa[17].split()[3].replace('.',''))
                result['tahapan_vaksinasi']['petugas_publik']['sudah_vaksin1'] = int(linesa[18].split()[2].replace('.',''))
                result['tahapan_vaksinasi']['petugas_publik']['sudah_vaksin2'] = int(linesa[18].split()[3].replace('.',''))
                result['tahapan_vaksinasi']['petugas_publik']['tertunda_vaksin1'] = int(linesa[19].split()[1].replace('.',''))
                result['tahapan_vaksinasi']['petugas_publik']['tertunda_vaksin2'] = int(linesa[19].split()[2].replace('.',''))
                result['tahapan_vaksinasi']['lansia'] = {}
                result['tahapan_vaksinasi']['lansia']['total_vaksinasi1'] = int(linesa[20].split()[1].replace('.',''))
                result['tahapan_vaksinasi']['lansia']['total_vaksinasi2'] = int(linesa[20].split()[2].replace('.',''))
                result['tahapan_vaksinasi']['lansia']['sudah_vaksin1'] = int(linesa[21].split()[2].replace('.',''))
                result['tahapan_vaksinasi']['lansia']['sudah_vaksin2'] = int(linesa[21].split()[3].replace('.',''))
                result['tahapan_vaksinasi']['lansia']['tertunda_vaksin1'] = int(linesa[22].split()[1].replace('.',''))
                result['tahapan_vaksinasi']['lansia']['tertunda_vaksin2'] = int(linesa[22].split()[2].replace('.',''))
                result['cakupan'] = {}
                result['cakupan']['vaksinasi1'] = linesa[26].split()[0]
                result['cakupan']['vaksinasi2'] = linesa[26].split()[1]
                result['cakupan']['sdm_kesehatan_vaksinasi1'] = linesa[28].split()[2]
                result['cakupan']['sdm_kesehatan_vaksinasi2'] = linesa[28].split()[3]
                result['cakupan']['petugas_publik_vaksinasi1'] = linesa[30].split()[2]
                result['cakupan']['petugas_publik_vaksinasi2'] = linesa[30].split()[3]
                result['cakupan']['lansia_vaksinasi1'] = lines[31].split()[1]
                result['cakupan']['lansia_vaksinasi2'] = lines[31].split()[2]
                result['date'] = dateparser.parse(linesa[8].split(",")[1]).strftime('%Y-%m-%d')
        else:
            result['total_sasaran_vaksinasi'] = target
            result['sasaran_vaksinasi_sdmk'] = extract(lines,6)
            result['sasaran_vaksinasi_petugas_publik'] = extract(lines,8)
            result['sasaran_vaksinasi_lansia'] = extract(lines, 9)
            
            result['vaksinasi1'] = int(linesa[11].replace('.',''))
            result['vaksinasi2'] = int(linesa[15].replace('.',''))
            result['tahapan_vaksinasi'] = {}
            result['tahapan_vaksinasi']['sdm_kesehatan'] = {}
            if linesa[13] == 'Vaksinasi-2':
                result['tahapan_vaksinasi']['sdm_kesehatan']['total_vaksinasi1'] = int(sanitize(linesa[17].split()[1]))
                result['tahapan_vaksinasi']['sdm_kesehatan']['total_vaksinasi2'] = int(sanitize(linesa[17].split()[2]))
                result['tahapan_vaksinasi']['sdm_kesehatan']['sudah_vaksin1'] = int(linesa[17].split()[2].replace('.',''))
                result['tahapan_vaksinasi']['sdm_kesehatan']['sudah_vaksin2'] = int(linesa[17].split()[3].replace('.',''))
                result['tahapan_vaksinasi']['sdm_kesehatan']['tertunda_vaksin1'] = int(linesa[18].split()[1].replace('.',''))
                result['tahapan_vaksinasi']['sdm_kesehatan']['tertunda_vaksin2'] = int(linesa[18].split()[2].replace('.',''))
                result['tahapan_vaksinasi']['petugas_publik'] = {}
                result['tahapan_vaksinasi']['petugas_publik']['total_vaksinasi1'] = int(linesa[20].split()[1].replace('.',''))
                result['tahapan_vaksinasi']['petugas_publik']['total_vaksinasi2'] = int(linesa[20].split()[2].replace('.',''))
                result['tahapan_vaksinasi']['petugas_publik']['sudah_vaksin1'] = int(linesa[21].split()[2].replace('A','4').replace('T','7').replace('.',''))
                result['tahapan_vaksinasi']['petugas_publik']['sudah_vaksin2'] = int(linesa[21].split()[3].replace('.',''))
                #result['tahapan_vaksinasi']['petugas_publik']['tertunda_vaksin1'] = int(linesa[22].split()[1].replace('.',''))
                #result['tahapan_vaksinasi']['petugas_publik']['tertunda_vaksin2'] = int(linesa[22].split()[2].replace('.',''))
                result['tahapan_vaksinasi']['lansia'] = {}
                
                if 'Lansia' in linesa[25]:
                    if len(linesa[25].split()) > 2:
                        result['tahapan_vaksinasi']['lansia']['total_vaksinasi1'] = int(linesa[25].split()[1].replace('.',''))
                        result['tahapan_vaksinasi']['lansia']['total_vaksinasi2'] = int(linesa[25].split()[2].replace('.',''))
                else:
                    if len(linesa[23].split()) > 1:
                        result['tahapan_vaksinasi']['lansia']['total_vaksinasi1'] = int(linesa[23].split()[2].replace('.',''))
                    else:
                        result['tahapan_vaksinasi']['lansia']['total_vaksinasi1'] = int(linesa[23].split()[1].replace('.',''))
                    if len(linesa[23].split()) > 3:
                        result['tahapan_vaksinasi']['lansia']['total_vaksinasi2'] = int(linesa[23].split()[3].replace('.',''))
                    else:
                        result['tahapan_vaksinasi']['lansia']['total_vaksinasi2'] = 0
                    try:
                        result['tahapan_vaksinasi']['lansia']['sudah_vaksin1'] = int(linesa[24].split()[2].replace('.',''))
                    except:
                        pass
                    if len(linesa[24].split()) > 3:
                        result['tahapan_vaksinasi']['lansia']['sudah_vaksin2'] = int(linesa[24].split()[3].replace('.',''))
                    else:
                        result['tahapan_vaksinasi']['lansia']['sudah_vaksin2'] = 0
                #result['tahapan_vaksinasi']['lansia']['tertunda_vaksin1'] = int(linesa[22].split()[1].replace('.',''))
                #result['tahapan_vaksinasi']['lansia']['tertunda_vaksin2'] = int(linesa[22].split()[2].replace('.',''))
                result['cakupan'] = {}
                if lines[29] == 'Vaksinasi-1 Vaksinasi-2':
                    result['cakupan']['vaksinasi1'] = lines[30].split()[0]
                    result['cakupan']['vaksinasi2'] = lines[30].split()[1]
                    result['cakupan']['sdm_kesehatan_vaksinasi1'] = lines[32].split()[1]
                    result['cakupan']['sdm_kesehatan_vaksinasi2'] = lines[32].split()[2]
                    result['cakupan']['petugas_publik_vaksinasi1'] = lines[34].split()[2]
                    result['cakupan']['petugas_publik_vaksinasi2'] = lines[34].split()[3]

                else:
                    result['cakupan']['vaksinasi1'] = lines[29].split()[0]
                    result['cakupan']['vaksinasi2'] = lines[29].split()[1]
                    result['cakupan']['sdm_kesehatan_vaksinasi1'] = lines[31].split()[1]
                    result['cakupan']['sdm_kesehatan_vaksinasi2'] = lines[31].split()[2]
                    result['cakupan']['petugas_publik_vaksinasi1'] = lines[33].split()[1]
                    result['cakupan']['petugas_publik_vaksinasi2'] = lines[33].split()[2]
                #result['cakupan']['lansia_vaksinasi1'] = lines[31].split()[1]
                #result['cakupan']['lansia_vaksinasi2'] = lines[31].split()[2]
                result['date'] = dateparser.parse(lines[8]).strftime('%Y-%m-%d')
    return result
