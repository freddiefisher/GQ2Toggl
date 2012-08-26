Command-line app for exporting GQueues Task Lists to Toggl Time Tracking. 

I recommend you read the step-by-step ' GQ2Toggl Manual.pdf ', which includes screenshots and diagrams. 



USAGE SUMMARY : 

1. Click to export a Queue in GQueues.
2. Download CSV to default location. 
3. Run GQ2Toggl.
4. Follow onscreen instructions



HIERARCHY MATCHING : 

GQueues allows unlimited task nesting. However, Toggl only allows Projects, and Tasks. 

Thus, a few different options are availible for flattening GQueues hierarchies. 

First, you can decide if the GQueues Task List should represent a single Toggl project, or multiple projects.

Second, there are 3 ways of reconciling any remaining hierarchy mis-match. 

1. ' Flatten Leaves '     - convert task hierarchy to a flat list. 
2. ' Emulate Hierarchy '  - use a naming convention to emulate original hierarchy. 
3. ' Root Tasks Only '    - only export top-level tasks to Toggl.

You can see examples of these methods in the included manual. 



DEPENDENCY NOTICE : 

This app requires the python ' requests ' module. 

In Ubuntu, you can install the package python-requests in synaptic.

Otherwise you can pip or easyinstall ' requests '. 
