# should be run from within the 'testing' directory, otherwise adjust pathnames

python3 ../qatools.py --subjects_dir data --output_dir output/test001 --subjects 091

python3 ../qatools.py --subjects_dir data --output_dir output/test002 --subjects 129 130

python3 ../qatools.py --subjects_dir data --output_dir output/test003

python3 ../qatools.py --subjects_dir data --output_dir output/test004 --screenshots

python3 ../qatools.py --subjects_dir data --output_dir output/test005 --fornix

python3 ../qatools.py --subjects_dir data --output_dir output/test006 --outlier

python3 ../qatools.py --subjects_dir data --output_dir output/test007 --outlier --outlier-table data/buckner_AsegExampleNorms.csv

python3 ../qatools.py --subjects_dir data --output_dir output/test008 --screenshots --fornix --outlier

python3 ../qatools.py --subjects_dir data --output_dir output/test009 --subjects 129 130 --screenshots

python3 ../qatools.py --subjects_dir data --output_dir output/test010 --subjects 129 130 --screenshots --screenshots_views x=10 x=-10 y=0 z=0

python3 ../qatools.py --subjects_dir data --output_dir output/test011 --subjects 129 130 --screenshots --screenshots_views z=10 y=-5 --screenshots-html

python3 ../qatools.py --subjects_dir data --output_dir output/test012 --screenshots --subjects 129 --screenshots_base data/129/mri/orig.mgz --screenshots_overlay none

python3 ../qatools.py --subjects_dir data --output_dir output/test013 --screenshots --subjects 129 --screenshots_overlay data/129/mri/aparc+aseg.mgz

python3 ../qatools.py --subjects_dir data --output_dir output/test014 --screenshots --subjects 129 --screenshots_overlay none --screenshots_surf data/129/surf/lh.white

python3 ../qatools.py --subjects_dir data --output_dir output/test015 --screenshots --subjects 129 --screenshots_overlay none --screenshots_surf data/129/surf/rh.white data/129/surf/lh.pial

python3 ../qatools.py --subjects_dir data --output_dir output/test016 --screenshots --outlier --fornix --shape --fornix-html

python3 ../qatools.py --subjects_dir data --output_dir output/test017 --subjects-file subjects.lst

python3 ../qatools.py --subjects_dir data --output_dir output/test018 --subjects 129 130 --screenshots --screenshots_views z=10 y=-5 --screenshots_layout 2 1

python3 ../qatools.py --subjects_dir data --output_dir output/test019 --subjects 129 130 --screenshots --screenshots_views z=10 y=-5 z=-10 y=5 x=0 --screenshots_layout 1 5 --screenshots-html

python3 ../qatools.py --subjects_dir data --output_dir output/test020 --fornix --fornix-html

python3 ../qatools.py --subjects_dir data --output_dir output/test021 --screenshots --subjects 129 130 --screenshots_base orig.mgz --screenshots_overlay none --screenshots-html

python3 ../qatools.py --subjects_dir data --output_dir output/test022 --screenshots --subjects 129 130 --screenshots_overlay aparc+aseg.mgz --screenshots-html

python3 ../qatools.py --subjects_dir data --output_dir output/test023 --screenshots --subjects 129 130 --screenshots_overlay none --screenshots_surf lh.white --screenshots-html

python3 ../qatools.py --subjects_dir data --output_dir output/test024 --screenshots --subjects 129 130 --screenshots_base orig.mgz --screenshots_surf lh.pial rh.white --screenshots-html

python3 ../qatools.py --subjects_dir data --output_dir output/test025 --hypothalamus

python3 ../qatools.py --subjects_dir data --output_dir output/test026 --screenshots --hypothalamus-html --screenshots-html --fornix-html --hippocampus-html --outlier --hippocampus-label T1.v21

python3 ../qatools.py --subjects_dir data --output_dir output/test027 --hippocampus --hippocampus-label T1.v21

python3 ../qatools.py --subjects_dir data --output_dir output/test028 --surfaces --subjects 129 130

python3 ../qatools.py --subjects_dir data --output_dir output/test029 --surfaces-html --subjects 129 130

python3 ../qatools.py --subjects_dir data --output_dir output/test030 --skullstrip --subjects 129 130

python3 ../qatools.py --subjects_dir data --output_dir output/test031 --skullstrip-html --subjects 129 130
