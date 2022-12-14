
## Site aws - Elastic Kubernetes Service (Amazon EKS)

### Criar cluster
```
$ eksctl create cluster \
    --name=kubea3datak1 \
    --version=1.21 \
    --managed \
    --instance-types=m5.xlarge \
    --alb-ingress-access --node-private-networking \
    --region=us-east-1 \
    --nodes-min=2 --nodes-max=3 \
    --full-ecr-access \
    --asg-access \
    --nodegroup-name=ng-kubea3datak1 \
    --timeout=60m
```

### Ver cluster
```
Listar clustes aws
$ kubectl get nodes

Ver namespace
# kubectl get ns

```

### Criar namespace
```
$ kubectl create namespace airflowk1
```

## Criar parta no vscode rais chamada: airflow_k2k

### Installing the Chart

```
$ helm repo add apache-airflow https://airflow.apache.org
$ helm show values apache-airflow/airflow >> airflowk1/custom_values.yaml
```

# Configurar custom_values.yaml, alterar linhas
alterar custom_values.yaml

# Instalar hell no airflow
Comecar o deployment do airflow, comeca a instalacao no cluster kubernetes

```
$ helm install airflow apache-airflow/airflow \
    -f airflowk1/custom_values.yaml \
    -n airflowk1 \
    --create-namespace \
    --version 1.7.0 \
    --timeout 5m \
    --debug
```

listar se esta rodando››
```
$ kubectl get pods -n airflowk1
```

listar os clusters
```
$ kubectl get svc -n airflowk1
```

# pagina web
```
$ kubectl get pods -n airflowk1
$ kubectl get svc -n airflowk1
```

Colocar o caminho do DNS publico, que aparece no LoadBalancer, nao esquecer a porta :8080

exemplo: a9af38c59f809435bb8f7b0cad44c0a0-439410570.us-east-1.elb.amazonaws.com:8080
user: kelly.lyra
senha: admin

## resetar a senha
- entrar em perfil, menu superior direito
- resetar a senha
- fazer logout e logar novamente com a senha nova

##  persisitir kubernete
caso caia ele se recupera contra falha.

cria uam conexao com o disco externo e persisite os dados no pods, mesmo que caia ele recupera o ultimo stage
```
$ kubectl get pvc -n airflow_k2k
```
# Pagina web
## Criar nova conexao
exemplo: xpto.us-east-1.elb.amazonaws.com:8080
Admin\connection
- name: my_aws  # o que ta no arquivo de config
- connection Type: Amazon Web Service
- Login: xxx # access key ID
- Password:  xxx # secrets access key

## Criar variaveis de ambiente
Admin\variables

var 1
- key: aws_access_key_id
- val: access key ID
- description: Access Key para AWS

var2
- key: aws_secrets_access_key
- val: xxx # secrets access key
- description: Secrets Access Key para AWS

## emr >> EC2
### criar ke pair

### criar security group
 ass regla permitindo SSH

# programacao
- apos desenvolver o codigo, copiar arquivo .py para  aws

- adicionar no git hub

## logs aws

** IMPORTANTE** 
- LISTAR O .SHOW()
- Adicionar SSH no VPC - IP


```
$ ssh -i ec2-kellylyra.pem hadoop@ec2-52-23-220-141.compute-1.amazonaws.com
```

## Lista todas as plicacoes que rodaram
```
$ yarm app -list -appStates ALL
```
copiar id State

## exibir logs no erm
```
# yarm logs-applicationId {State}
```

## para sair 
```
# exit
```

# DESLIGAR CLUSTER ERM
NO SITE AWS

# DESLIGAR CLUSTER KUBERNETES

## listar pods ativos
```
$ kubectl get pods -n airflow
```

## IMPORTATE - Desistalando o airflow e todos os recursos associados
```
$ helm delete airflow -n airflowk1
```

## listar status dos recursos
garantir que esta sendo removido

- loadbalance
```
$ kubectl get svc -n airflowk1
```
caso nao remova, fazer manualmente
```
$ kubectl delete svc --all -n airflowk1
```

- pvc
```
$ kubectl get pvc -n airflowk1
```
caso nao remova, fazer manualmente
```
$ kubectl delete pvc --all -n airflowk1
```

# Deletar as stacks no CloudFormation

```
$ eksctl delete cluster --region=us-east-1 --name=kubea3datak1
```
