import os

JOB_STATUS_TYPES = ['CREATED','IN_PROGRESS','COMPLETE','COMPLETE_WITH_ERRORS']

PLUGINS = ['Vaa3D_Neuron2', 'Vaa3D-FarSight_snake_tracing']

OUTPUT_FILE_SUFFIXES = {
	'Vaa3D_Neuron2': '_x72_y57_z64_app2.swc',
	'Vaa3D-FarSight_snake_tracing' : '_snake.swc'
}


JOB_TYPES = ['Neuron Tracing', 'Neuron Utilities']
JOB_TYPE_PLUGINS = {
          'Neuron Tracing' : ['Vaa3D_Neuron2','Vaa3D-FarSight_snake_tracing'],
          'Neuron Utilities' : ['None Available']
}
PLUGINS = [
	{ 
	'name' : 'Vaa3D_Neuron2',
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
            'values' : ['app1', 'app2'],
            'default' : 'app2'
     }
  },
  {
  'name': 'Vaa3D-FarSight_snake_tracing',
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
        'values' : ['snake_trace'],
        'default' : 'snake_trace'
 	}                  
  }
]