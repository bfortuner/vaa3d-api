import os
from bigneuron_app.clients.constants import *

JOB_STATUS_TYPES = ['CREATED','IN_PROGRESS','COMPRESSING_FILES','COMPLETE','COMPLETE_WITH_ERRORS']
PROCESS_JOBS_CREATED_TASK='process_jobs_created'
PROCESS_JOBS_IN_PROGRESS_TASK='process_jobs_in_progress'

OUTPUT_FILE_SUFFIXES = {
	'Vaa3D_Neuron2': '_app2.swc',
	'Vaa3D-FarSight_snake_tracing' : '_snake.swc',
	'SimpleAxisAnalyzer' : '_axis_analyzer.swc',
	'CWlab_method1_version1' : '_Cwlab_ver1.swc',
	'MST_tracing' : '_MST_Tracing.swc',   #error on Mac
	'MOST_tracing' : '_MOST.swc',
	'neuTube' : '_neutube.swc',
	'TReMap' : '_XY_3D_TreMap.swc', #timeout on mac after 200 seconds
	'fastmarching_spanningtree' : '_fastmarching_spanningtree.swc',    #timeout on mac
	'BJUT_meanshift' : '_meanshift.swc',
	'LCM_boost' : '_LCM_boost.swc',  #can't find this plugin on Mac
	'Advantra' : '_Advantra.swc',  #timeout on mac
	'nctuTW' : '_nctuTW.swc', #can't include -p flag
	'NeuronChaser' : '_NeuronChaser.swc',
	'NeuroStalker' : '_NeuroStalker.swc', #killed on mac
	'neutu_autotrace' : '_neutu_autotrace.swc',
	'smartTrace' : '_smartTracing.swc', #killed on mac
	'tips_GD' : '_nctuTW_GD.swc',
	'EnsembleNeuronTracerBasic' : '_EnsembleNeuronTracerBasic.swc',
	'EnsembleNeuronTracerV2n' : '_EnsembleNeuronTracerV2n.swc',
	'EnsembleNeuronTracerV2s' : '_EnsembleNeuronTracerV2s.swc',
	'SimpleTracing' : '_simple.swc',
	'anisodiff_littlequick' : '_anisodiff.raw'
}

JOB_TYPES = ['Neuron Tracing', 'Image Filtering', 'Neuron Utilities']

JOB_TYPE_PLUGINS = {
	'Neuron Tracing' : [
		'Vaa3D_Neuron2',
		'Vaa3D-FarSight_snake_tracing',
		'SimpleAxisAnalyzer',
		'CWlab_method1_version1',
		'MST_tracing', #fails on mac
		'MOST_tracing',
		'neuTube',
		'TReMap',
		'fastmarching_spanningtree',
		'BJUT_meanshift',
		'LCM_boost',
		'Advantra',
		'nctuTW',
		'NeuronChaser',
		'NeuroStalker',
		'neutu_autotrace',
		'smartTrace',
		'tips_GD',
		'EnsembleNeuronTracerBasic',
		'EnsembleNeuronTracerV2n',
		'EnsembleNeuronTracerV2s',
		'SimpleTracing'
	],
	'Neuron Utilities' : [
		'None Available'
	],
	'Image Filtering' : [
		'anisodiff_littlequick'
	]
}

PLUGINS = {
	'Vaa3D_Neuron2' : {
		'settings' : { 
	        'flag' : '-p',
	        'order' : ['channel'],
	        'params': { 
               'channel' : {
                	'values' : ['1','2','3'],
                	'default' : '1'
               }
            }
	    },
	    'method' : {
	        'values' : ['app2','app1'],
            'default' : 'app2'
	    },
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }
  	},
  	'Vaa3D-FarSight_snake_tracing' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
					'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['snake_trace'],
	    	'default' : 'snake_trace'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }                  
	},
  	'SimpleAxisAnalyzer' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['medial_axis_analysis'],
	    	'default' : 'medial_axis_analysis'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }                  
	},
  	'CWlab_method1_version1' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['tracing_func'],
	    	'default' : 'tracing_func'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }                  
	},
  	'MST_tracing' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['trace_mst'],
	    	'default' : 'trace_mst'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }                  
	},
  	'MOST_tracing' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['MOST_trace'],
	    	'default' : 'MOST_trace'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }                  
	},
  	'neuTube' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['neutube_trace'],
	    	'default' : 'neutube_trace'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }                  
	},
  	'TReMap' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['trace_mip'],
	    	'default' : 'trace_mip'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }                  
	},
  	'fastmarching_spanningtree' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['tracing_func'],
	    	'default' : 'tracing_func'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }                  
	},
  	'BJUT_meanshift' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['meanshift'],
	    	'default' : 'meanshift'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }                  
	},
  	'LCM_boost' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['LCM_boost'],
	    	'default' : 'LCM_boost'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }                  
	},
  	'Advantra' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['12 0.5 99 0.6 5 60 30 5 1'],
					'default' : '12 0.5 99 0.6 5 60 30 5 1'
				}
			}
		},
		'method' : {
	    	'values' : ['advantra_func'],
	    	'default' : 'advantra_func'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }                  
	},
  	'nctuTW' : {
		'settings' : {},
		'method' : {
	    	'values' : ['tracing_func'],
	    	'default' : 'tracing_func'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }                  
	},
  	'NeuronChaser' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1 10 90 0.6 15 60 30 5 1 0'],
					'default' : '1 10 90 0.6 15 60 30 5 1 0'
				}
			}
		},
		'method' : {
	    	'values' : ['nc_func'],
	    	'default' : 'nc_func'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }                  
	},
  	'NeuroStalker' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1 1 1 5 5 30'],
					'default' : '1 1 1 5 5 30'
				}
			}
		},
		'method' : {
	    	'values' : ['tracing_func'],
	    	'default' : 'tracing_func'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }
	},
  	'neutu_autotrace' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['tracing'],
	    	'default' : 'tracing'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }
	},
  	'smartTrace' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['smartTrace'],
	    	'default' : 'smartTrace'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }
	},
  	'tips_GD' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['tracing_func'],
	    	'default' : 'tracing_func'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }
	},
  	'EnsembleNeuronTracerBasic' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['tracing_func'],
	    	'default' : 'tracing_func'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }
	},
  	'EnsembleNeuronTracerV2n' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['tracing_func'],
	    	'default' : 'tracing_func'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }
	},
  	'EnsembleNeuronTracerV2s' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['tracing_func'],
	    	'default' : 'tracing_func'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }
	},
  	'SimpleTracing' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['tracing','ray_shooting','dfs'],
	    	'default' : 'tracing'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }
	},
	'anisodiff_littlequick' : {
		'settings' : { 
		    'flag' : '-p',
		    'order' : ['channel'],
		    'params': { 
				'channel' : {
	              	'values' : ['1'],
					'default' : '1'
				}
			}
		},
		'method' : {
	    	'values' : ['anisodiff_littlequick_func'],
	    	'default' : 'anisodiff_littlequick_func'
		},
	    'runtime' : {
	    	'max' : VAA3D_MAX_RUNTIME,
	    	'min' : VAA3D_MIN_RUNTIME,
	    	'bytes_per_sec' : BASE_BYTES_PER_SEC
	    }
	}
}