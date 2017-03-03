How to add Mongo database in container:

Based on instructions at https://github.com/kubernetes/kubernetes/tree/master/examples/nodesjs-mongodb

kubectl create -f mongo-service.yaml
kubectl create -f mongo-pv.yaml
kubectl create -f mongo-controller.yaml
