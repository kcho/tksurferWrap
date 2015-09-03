#!/ccnc_bin/venv/bin/python2.7
import re
import sys
import os
import shutil
import argparse
import textwrap
import getpass

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def freesurferSetEnv(directory):
    os.environ["FREESURFER_HOME"] = '/Applications/freesurfer'
    os.environ["SUBJECTS_DIR"] = directory

def get_freesurfer_directory(directory):
    subject = []
    for root,dirs,files in walklevel(directory):
        if 'bem' in dirs and 'label' in dirs and 'mri' in dirs and 'scripts' in dirs and 'surf' in dirs:
            subject.append(os.path.basename(root))

    if len(subject) != 1:
        oneSubject = raw_input(', '.join(subject) + ' choose one subject  :')
        return oneSubject
    else:
        return subject[0]

def annot2label(subject,side):
    command = 'mri_annotation2label \
            --subject {subject} \
            --hemi {side} \
            --outdir {outdir}'.format(subject = subject,
                    side = side,
                    outdir = os.getcwd())
    command = re.sub('\s+',' ',command)
    print '\t'+command
    os.popen(command).read()

def label2annot(location, subject,side,labelList):
    if os.path.isfile(os.path.join(location,subject,'label',side+'.kscript.annot')):
        os.remove(os.path.join(location,subject,'label',side+'.kscript.annot'))

    colortable = os.path.join(os.getcwd(),'ctab.txt')
    command = 'mris_label2annot \
            --subject {subject} \
            --hemi {side} \
            --a {name} \
            --ctab {colortable}'.format(subject = subject,
                    side = side,
                    name = 'kscript',
                    colortable = colortable)

    for label in labelList:
        print label
        labelFile = ''.join([x for x in os.listdir(os.getcwd()) if x.endswith('.'+label+'.label')])
        print labelFile
        command = command + ' --l '+labelFile

    command = re.sub('\s+',' ',command)
    print '\t'+command
    os.popen(command).read()

def bigROIchange(roiline):
    roiline = re.sub('OFC',"parsorbitalis,medialorbitofrontal,lateralorbitofrontal",roiline)
    roiline = re.sub('MPFC',"caudalanteriorcingulate, rostralanteriorcingulate, superiorfrontal",roiline)
    roiline = re.sub('LPFC',"parstriangularis, rostralmiddlefrontal, frontalpole, parsopercularis",roiline)
    roiline = re.sub('SMC',"precentral,caudalmiddlefrontal,postcentral,paracentral",roiline)
    roiline = re.sub('PC',"inferiorparietal,supramarginal,precuneus,posteriorcingulate,isthmuscingulate,superiorparietal",roiline)
    roiline = re.sub('MTC',"entorhinal,parahippocampal,fusiform",roiline)
    roiline = re.sub('LTC',"transversetemporal,superiortemporal,bankssts,inferiortemporal,middletemporal,temporalpole",roiline)
    roiline = re.sub('OCC',"pericalcarine,lingual,lateraloccipital,cuneus",roiline)
    roiline = re.sub('\s+','',roiline)
    return roiline


def makeColorTable(labelList,color,side):
    toWrite_header = '#$Id: FreeSurferColorLUT.txt,v 1.38.2.1 2007/08/20 01:52:07 nicks Exp $\n\
#No. Label Name:                            R   G   B   A\n'
#0   Unknown                                 0   0   0   0' + '\n'

    toWrite_body = ''
    user_name = getpass.getuser()
    try:
        with open('/Users/{0}/FreeSurferColorLUT.txt'.format(user_name),'rb') as f:
            lines = f.readlines()
    except:
        with open('/Applications/freesurfer/FreeSurferColorLUT.txt'.format(user_name),'rb') as f:
            lines = f.readlines()


    if side == 'lh':
        lines = lines[430:466]
    else:
        lines = lines[466:503]

    for num,label in enumerate(labelList):
        foundLine = ''.join([x for x in lines if side+'-'+label in x])

        #number change
        foundLine = re.sub('^\d{4}',str(num+1),foundLine)
        #colour change
        foundLine = re.sub('\d{1,3}\s+\d{1,3}\s+\d{1,3}\s+0.*$',
                color + ' 0',foundLine)

        toWrite_body = toWrite_body+''.join(foundLine)

    #for num,label in enumerate(labelList):
        #line = '{num}   {label}                  {color}  0'.format(num = num+1,
            #label = label,
            #color = color)
        #toWrite_body = toWrite_body+line+'\n'

    toWrite_merged = toWrite_header + toWrite_body

    with open(os.path.join(os.getcwd(),'ctab.txt'),'wb') as f:
        f.write(toWrite_merged)


def catchLabelList(comma_sep_labelList):
    toList = comma_sep_labelList.strip().split(',')

    #allLabels = [x for x in os.listdir(os.getcwd()) if x.endswith('label')]

    #labelList_formatted=[]
    #for label in toList:
        #labelList_formatted.append(re.search('\w{2}\.'+label+'\.label',
            #' '.join(allLabels),
            #re.IGNORECASE).group(0))

    #return labelList_formatted
    return toList

def main(args):
    # Set environment
    freesurferSetEnv(args.subjectDirectory)

    # Search directories with mri, scripts, labels
    if args.subject:
        subject = args.subject
    else:
        subject = get_freesurfer_directory(args.subjectDirectory)
    print subject

    # run annot2label using the label input
    annot2label(subject,args.side)


    labelList_initial = bigROIchange(args.labelList)
    # format the label list
    labelList_formatted = catchLabelList(labelList_initial)

    # make color table
    makeColorTable(labelList_formatted,args.color,args.side)

    # merge them back to annot
    label2annot(args.subjectDirectory,subject,args.side,labelList_formatted)
    removeList = [x for x in os.listdir(os.getcwd()) if x.endswith('label') or x =='surfer.log']
    for i in removeList:
        os.remove(os.path.join(os.getcwd(),i))

    # print tksurfer command
    print '\texport SUBJECTS_DIR={0}'.format(args.subjectDirectory)
    command = 'tksurfer {0} {1} pial -annotation kscript'.format(subject,args.side)
    print '\t'+command
    os.popen(command)


if __name__=='__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
            description = textwrap.dedent('''\
                    {codeName} : Runs mri_annotation2label on the selected labels
                                 from mri/annot file
                                 and mris_label2annotaion merging back to annot file
                    ====================
                    '''.format(codeName=os.path.basename(__file__))))

            #epilog="By Kevin, 26th May 2014")
    parser.add_argument('-d','--subjectDirectory',
            help="SUBJECTS_DIR",
            default=os.getcwd())

    parser.add_argument('-i','--subject',
            help="SUBJECT")

    parser.add_argument('-s','--side',
            help="Side [ lh / rh ]",
            default='lh')

    parser.add_argument('-c','--color',
            help="color in RGB eg '255 0 0'",
            default = '255 0 0')

    parser.add_argument('-l','--labelList',
            help="List of labels in list format eg ['precentral','superior-temporal']")

    args = parser.parse_args()

    if not (args.side or args.labelList):
        parser.error('No action requested, add -s and -l (side and labels)')

    main(args)
