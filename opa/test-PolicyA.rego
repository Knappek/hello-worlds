package kubernetes.admission

test_no_limits {
   no_limits := {
     "request":{
       "kind":{
         "kind":"Deployment"
       },
       "operation":"CREATE",
       "object":{
         "spec":{
           "template": {
             "spec": {
               "containers": [
                 {
                   "name": "nginx-1",
                   "resources":{
                       "requests":{
                          "cpu": "10mi",
                          "memory": "10mi"
                       }
                    }
                 }
               ]
             }
           }
         }
       }
     }
   }
   count(deny) == 1 with input as no_limits
 }

