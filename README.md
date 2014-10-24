# tksurferWrap

## Dependency
- freesurfer from http://freesurfer.net
- argparse module
- textwrap module
- shutil module

## Color tksurfer pial surface 
- It makes new annotation file within with the selected labels from aparc.annot file
- It's removed after the visualization with tksurfer

## Usage
```
  tksurferWrap [-h] [-d SUBJECTDIRECTORY] [-i SUBJECT] [-s SIDE] [-c COLOR] [-l LABELLIST]

  eg)
  tksurferWrap -d /Volmes/promise/freesurfer -i NOR45 -s lh -c '0 162 255' -l precuneus, postcentral, paracentral
```

## Input label list
```
bankssts                
caudalanteriorcingulate 
caudalmiddlefrontal     
corpuscallosum          
cuneus                  
entorhinal              
fusiform                
inferiorparietal        
inferiortemporal        
isthmuscingulate        
lateraloccipital        
lateralorbitofrontal    
lingual                 
medialorbitofrontal     
middletemporal          
parahippocampal         
paracentral             
parsopercularis         
parsorbitalis           
parstriangularis        
pericalcarine           
postcentral             
posteriorcingulate      
precentral              
precuneus               
rostralanteriorcingulate
rostralmiddlefrontal    
superiorfrontal         
superiorparietal        
superiortemporal        
supramarginal           
frontalpole             
temporalpole            
transversetemporal      
insula                  
```
