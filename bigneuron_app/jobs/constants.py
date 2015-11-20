import os

JOB_STATUS_TYPES = ['CREATED','IN_PROGRESS','COMPLETE','COMPLETE_WITH_ERRORS']

OUTPUT_FILE_SUFFIXES = {
	'Vaa3D_Neuron2': '_x72_y57_z64_app2.swc',
	'Vaa3D-FarSight_snake_tracing' : '_snake.swc',
	'SimpleAxisAnalyzer' : '_axis_analyzer.swc',
	'CWlab_method1_version1' : '_Cwlab_ver1.swc',
	'MST_tracing' : '_MST_Tracing.swc'
}

JOB_TYPES = ['Neuron Tracing', 'Neuron Utilities']

JOB_TYPE_PLUGINS = {
	'Neuron Tracing' : ['Vaa3D_Neuron2','Vaa3D-FarSight_snake_tracing',
						'SimpleAxisAnalyzer','CWlab_method1_version1','MST_tracing'],
	'Neuron Utilities' : ['None Available']
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
	        'values' : ['app2'],
            'default' : 'app2'
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
		}                  
	}
}