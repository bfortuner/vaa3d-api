#!/bin/bash
#
#This is a shell program to batch reconstruct images using 28 different methods.
#
# Last change: 2015-08-17. by Hanchuan Peng adding the anisotropic filtering. 
#

function write_neuron_tracing_command {

  outputScript=$1;
  METHOD=$2;
  vaa3dProgramPath=$3;
  inimgfileTracing=$4;
  finalfileFolder=$5;

  smooth_inimgfileTracing=${inimgfileTracing}.g.v3draw;

#smooth image only - only takes .raw files?

  if [ $METHOD == "smooth" ]; then
   echo "./start_vaa3d.sh -x gaussian -f gf -i $inimgfileTracing -o $smooth_inimgfileTracing -p 7 7 2 1 2;./start_vaa3d.sh -x datatypeconvert -f dtc -i $smooth_inimgfileTracing -o $smooth_inimgfileTracing -p 1 ;chmod -R 777 $smooth_inimgfileTracing;mv  $smooth_inimgfileTracing $finalfileFolder" >> $outputScript;
  fi;

#anisotropic filtering using littlequick version of Lei's plugin 

  if [ $METHOD == "aniso" ]; then
   echo "./start_vaa3d.sh -x anisodiff_littlequick -f anisodiff_littlequick_func -i $inimgfileTracing;chmod -R 777 $inimgfileTracing*_anisodiff.raw;mv  $inimgfileTracing*_anisodiff.raw $finalfileFolder" >> $outputScript;
  fi;

#APP1 - added

  if [ $METHOD == "1" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x vn2 -f app1 -i $inimgfileTracing -p NULL 0 40 1;chmod -R 777 $inimgfileTracing*_app1.swc;mv  $inimgfileTracing*_app1.swc $finalfileFolder" >> $outputScript;
  fi;

#APP2 - added

  if [ $METHOD == "2" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x vn2 -f app2 -i $inimgfileTracing -p NULL 0 10 1 1 0 0 5 0 0 0;chmod -R 777 $inimgfileTracing*_app2.swc;mv  $inimgfileTracing*_app2.swc $finalfileFolder;rm  $inimgfileTracing*_ini.swc" >> $outputScript;
  fi;

#MOST - added

  if [ $METHOD == "3" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x MOST -f MOST_trace -i $inimgfileTracing -p 1 40;chmod -R 777 $inimgfileTracing*_MOST.swc;mv  $inimgfileTracing*_MOST.swc $finalfileFolder" >> $outputScript;
  fi;

#NEUTUBE - added

  if [ $METHOD == "4" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x neuTube -f neutube_trace -i $inimgfileTracing -p 1 1;chmod -R 777 $inimgfileTracing*_neutube.swc;mv  $inimgfileTracing*_neutube.swc $finalfileFolder" >> $outputScript;
  fi;

#FARSIGHT Snake - added

  if [ $METHOD == "5" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x snake -f snake_trace -i $inimgfileTracing -p 1;chmod -R 777 $inimgfileTracing*_snake.swc;mv  $inimgfileTracing*_snake.swc $finalfileFolder" >> $outputScript;
  fi;

#3 from SimpleTracing - added

  if [ $METHOD == "6" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x SimpleTracing -f tracing -i $inimgfileTracing -o ${inimgfileTracing}_simple.swc -p 1;chmod -R 777 $inimgfileTracing*_simple.swc;mv  $inimgfileTracing*_simple.swc $finalfileFolder" >> $outputScript;
  fi;

  if [ $METHOD == "7" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x SimpleTracing -f ray_shooting -i $inimgfileTracing -o ${inimgfileTracing}_Rayshooting.swc;chmod -R 777 $inimgfileTracing*_Rayshooting.swc;mv  $inimgfileTracing*_Rayshooting.swc $finalfileFolder" >> $outputScript;
  fi;

  if [ $METHOD == "8" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x SimpleTracing -f dfs -i $inimgfileTracing -o ${inimgfileTracing}_Rollerball.swc;chmod -R 777 $inimgfileTracing*_Rollerball.swc;mv  $inimgfileTracing*_Rollerball.swc $finalfileFolder" >> $outputScript;
  fi;

#TreMap - added

  if [ $METHOD == "9" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x TReMap -f trace_mip -i $inimgfileTracing -p 0 1 10 0 1 0 5;chmod -R 777 $inimgfileTracing*_TreMap.swc;mv  $inimgfileTracing*_TreMap.swc $finalfileFolder" >> $outputScript;
  fi;

#MST - added

  if [ $METHOD == "10" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x MST_tracing -f trace_mst -i $inimgfileTracing -p 1 5;chmod -R 777 $inimgfileTracing*_MST_Tracing.swc;mv  $inimgfileTracing*_MST_Tracing.swc $finalfileFolder" >> $outputScript;
  fi;

#NeuroGPSTree - killed - probably need to clarify parameters

  if [ $METHOD == "11" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x NeuroGPSTree -f tracing_func -i $inimgfileTracing -p 1 1 1 10;chmod -R 777 $inimgfileTracing*_NeuroGPSTree.swc;mv  $inimgfileTracing*_NeuroGPSTree.swc $finalfileFolder" >> $outputScript;
  fi;

#fastmarching_spanningtree - added

  if [ $METHOD == "12" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x fastmarching_spanningtree -f tracing_func -i $inimgfileTracing ;chmod -R 777 $inimgfileTracing*_fastmarching_spanningtree.swc;mv  $inimgfileTracing*_fastmarching_spanningtree.swc $finalfileFolder" >> $outputScript;
  fi;

#meanshift - added

  if [ $METHOD == "13" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x BJUT_meanshift -f meanshift -i $inimgfileTracing ;rm  $inimgfileTracing*init_meanshift.swc;chmod -R 777 $inimgfileTracing*_meanshift.swc;mv  $inimgfileTracing*_meanshift.swc $finalfileFolder" >> $outputScript;
  fi;

#CWlab_method1_version1 - added

  if [ $METHOD == "14" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x CWlab_method1_version1 -f tracing_func -i $inimgfileTracing -p 1;chmod -R 777 $inimgfileTracing*_Cwlab_ver1.swc;mv  $inimgfileTracing*_Cwlab_ver1.swc $finalfileFolder" >> $outputScript;
  fi;

#LCM_boost - added

  if [ $METHOD == "15" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x LCM_boost -f LCM_boost -i $inimgfileTracing -o ${inimgfileTracing}_LCMboost.swc ;chmod -R 777 $inimgfileTracing*_LCMboost.swc;mv  $inimgfileTracing*_LCMboost.swc $finalfileFolder" >> $outputScript;
  fi;

#NeuroStalker - added

  if [ $METHOD == "16" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x NeuroStalker -f tracing_func -i $inimgfileTracing -p 1 1 1 5 5 30;chmod -R 777 $inimgfileTracing*_NeuroStalker.swc;mv  $inimgfileTracing*_NeuroStalker.swc $finalfileFolder" >> $outputScript;
  fi;

#nctuTW - added

  if [ $METHOD == "17" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x nctuTW -f tracing_func -i $inimgfileTracing -p NULL;chmod -R 777 $inimgfileTracing*_nctuTW.swc;mv  $inimgfileTracing*_nctuTW.swc $finalfileFolder" >> $outputScript;
  fi;

#tips_GD - added

  if [ $METHOD == "18" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x tips_GD -f tracing_func -i $inimgfileTracing ;chmod -R 777 $inimgfileTracing*_nctuTW_GD.swc;mv  $inimgfileTracing*_nctuTW_GD.swc $finalfileFolder" >> $outputScript;
  fi;

#SimpleAxisAnalyzer - added

  if [ $METHOD == "19" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x SimpleAxisAnalyzer -f medial_axis_analysis -i $inimgfileTracing;chmod -R 777 $inimgfileTracing*_axis_analyzer.swc;mv  $inimgfileTracing*_axis_analyzer.swc $finalfileFolder" >> $outputScript;
  fi;

#NeuronChaser - added

  if [ $METHOD == "20" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x NeuronChaser -f nc_func -i $inimgfileTracing -p 1 10 90 0.6 15 60 30 5 1 0;chmod -R 777 $inimgfileTracing*_NeuronChaser.swc;mv  $inimgfileTracing*_NeuronChaser.swc $finalfileFolder" >> $outputScript;
  fi;

#smartTracing - added

  if [ $METHOD == "21" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x smartTrace -f smartTrace -i $inimgfileTracing ;chmod -R 777 $inimgfileTracing*_smartTracing.swc;mv  $inimgfileTracing*_smartTracing.swc $finalfileFolder" >> $outputScript;
  fi;

#neutu_autotrace - added

  if [ $METHOD == "22" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x neutu_autotrace -f tracing -i $inimgfileTracing ;chmod -R 777 $inimgfileTracing*_neutu_autotrace.swc;mv  $inimgfileTracing*_neutu_autotrace.swc $finalfileFolder" >> $outputScript;
  fi;

#Advantra - added

  if [ $METHOD == "23" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x Advantra -f advantra_func -i $inimgfileTracing -p 10 0.3 95 0.6 15 60 30 5 1;chmod -R 777 $inimgfileTracing*_Advantra.swc;mv  $inimgfileTracing*_Advantra.swc $finalfileFolder" >> $outputScript;
  fi;

#RegMST - killed but need clarity on params

  if [ $METHOD == "24" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x RegMST -f tracing_func -i $inimgfileTracing -p $vaa3dProgramPath/filter_banks/oof_fb_3d_scale_1_2_3_5_size_13_sep_cpd_rank_49.txt  $vaa3dProgramPath/filter_banks/oof_fb_3d_scale_1_2_3_5_size_13_weigths_cpd_rank_49.txt $vaa3dProgramPath/filter_banks/proto_filter_AC_lap_633_822_sep_cpd_rank_49.txt $vaa3dProgramPath/filter_banks/proto_filter_AC_lap_633_822_weigths_cpd_rank_49.txt 1 2 $vaa3dProgramPath/trained_models/model_S/Regressor_ac_0.cfg $vaa3dProgramPath/trained_models/model_S/Regressor_ac_1.cfg 21 200 ;chmod -R 777 $inimgfileTracing*_tubularity_model_S.v3draw_MST_Tracing_Ws_21_th_200.swc;mv  $inimgfileTracing*_tubularity_model_S.v3draw_MST_Tracing_Ws_21_th_200.swc $finalfileFolder ;rm  $inimgfileTracing*_tubularity_model_S.v3draw" >> $outputScript; 
  fi;

#EnsembleNeuronTracer - added

  if [ $METHOD == "25" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x EnsembleNeuronTracerBasic -f tracing_func -i $inimgfileTracing ;chmod -R 777 $inimgfileTracing*_EnsembleNeuronTracerBasic.swc;mv  $inimgfileTracing*_EnsembleNeuronTracerBasic.swc $finalfileFolder" >> $outputScript;
  fi;

#EnsembleNeuronTracerV2n - added

  if [ $METHOD == "26" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x EnsembleNeuronTracerV2n -f tracing_func -i $inimgfileTracing ;chmod -R 777 $inimgfileTracing*_EnsembleNeuronTracerV2n.swc;mv  $inimgfileTracing*_EnsembleNeuronTracerV2n.swc $finalfileFolder" >> $outputScript;
  fi;

#EnsembleNeuronTracerV2s - added

  if [ $METHOD == "27" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x EnsembleNeuronTracerV2s -f tracing_func -i $inimgfileTracing ;chmod -R 777 $inimgfileTracing*_EnsembleNeuronTracerV2s.swc;mv  $inimgfileTracing*_EnsembleNeuronTracerV2s.swc $finalfileFolder" >> $outputScript;
  fi;

#3DTraceSWC - need params or maybe latest software?

  if [ $METHOD == "28" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x aVaaTrace3D -f func1 -i $inimgfileTracing -p 20 2 2.5;chmod -R 777 $inimgfileTracing*_pyzh.swc;mv  $inimgfileTracing*_pyzh.swc $finalfileFolder" >> $outputScript;
  fi;

#Rivulet - need params or maybe latest software?

  if [ $METHOD == "29" -o $METHOD == "-1" ]; then
    echo "./start_vaa3d.sh -x Rivulet -f tracing_func -i $inimgfileTracing ;chmod -R 777 $inimgfileTracing*_Rivulet.swc;mv  $inimgfileTracing*_Rivulet.swc.swc $finalfileFolder" >> $outputScript;
  fi;
}

if [ ! $# -ge 1 ]; then
	echo "sh gen_bench_job_scripts.sh  <tracing algorithm number> <input image path> <output folder path> <Vaa3D executable folder path>"
	exit
fi

#if [ $# -ge 2 ]; then
#	if [ ! -f $2 ]; then
#		echo "Can not find file [$2]"
#		exit
#	fi
#else
#	echo "sh gen_bench_job_scripts.sh  <tracing algorithm number> <input image path> <output folder path> <Vaa3D executable folder path>"
#	exit
#fi

if [ $# -ge 3 ]; then
	if [ ! -d $3 ]; then
		mkdir $3
	fi
else
	echo "sh gen_bench_job_scripts.sh  <tracing algorithm number> <input image path> <output folder path> <Vaa3D executable folder path>"
	exit
fi

if [ $# -ge 4 ]; then
        if [ ! -d $4 ]; then
                echo "Can not find Vaa3D executable folder [$4]"
                exit
        fi
else
        echo "sh gen_bench_job_scripts.sh  <tracing algorithm number> <input image path> <output folder path> <Vaa3D executable folder path>"
        exit
fi


#copy the names
tracingMethod=$1
inputImgFile=$2
finalfileFolder=$3
vaa3dProgramPath=$4
jobScriptFile=$5


#generate the batch script configuration
if [ -f $jobScriptFile ]; then
  rm $jobScriptFile;
fi;

#generate the actual tracing code
if [ ! -d $finalfileFolder ]; then
  mkdir $finalfileFolder
fi

write_neuron_tracing_command $jobScriptFile $tracingMethod $vaa3dProgramPath $inputImgFile $finalfileFolder