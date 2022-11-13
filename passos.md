# Exemplo professor
https://github.com/neylsoncrepalde/pucminas-data-pipelines

video
https://sgapucminasbr.sharepoint.com/:v:/r/sites/team_sal_iec_5102_2_1_89554/Documentos%20Compartilhados/General/Recordings/Exibir%20Apenas/Meeting%20in%20_General_-20221006_190811-Meeting%20Recording.mp4?csf=1&web=1&e=vXhUAW

https://sgapucminasbr.sharepoint.com/:v:/r/sites/team_sal_iec_5102_2_1_89554/Documentos%20Compartilhados/General/Recordings/Exibir%20Apenas/Meeting%20in%20_General_-20220922_190342-Meeting%20Recording.mp4?csf=1&web=1&e=GqNXtP


# Passo a passo trabalho final

## INSTALACAO 
### ✅ Instalar  kubectl

```
$ brew install kubectl 
```

### ✅ Instalar helm
```
$ brew install helm
```

### ✅ Instalar eksctl
```
$ brew tap weaveworks/tap
$ brew install weaveworks/tap/eksctl
```

### ✅ Instalar awscli
```
$ curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
$ sudo installer -pkg AWSCLIV2.pkg -target /
```

## CONFIGURAR CONTA AWS 
### ✅ site AWS
- Cria um usuario com permissao de administrador: 
arn:aws:iam::107573687852:user/pucminas
- Criar Certificado para o usuario SSH

## ✅ Terminal vscode
- Configurar ceriticado aws SSH
```
$ aws configure
AWS Access Key ID [None]: ...KJH4J
AWS Secret Access Key [None]: ...7XXQv
Default region name [None]: us-east-1
Default output format [None]: json
```

###✅ testar conexao aws 
```
$ aws ls s3
```

## Site aws - Elastic Kubernetes Service (Amazon EKS)

### Criar cluster
```
$ eksctl create cluster \
    --name=kubea3datak2k \
    --version=1.21 \
    --managed \
    --instance-types=m5.xlarge \
    --alb-ingress-access --node-private-networking \
    --region=us-east-1 \
    --nodes-min=2 --nodes-max=3 \
    --full-ecr-access \
    --asg-access \
    --nodegroup-name=ng-kubea3datak2k \
    --timeout=60m
```
### Listar os contextos instanciados
```
$ kubectl config get-contexts
```

### Listar clustes aws
```
$ kubectl get nodes
```

### Criar namespace
```
$ kubectl create namespace airflow8
```

### Ver namespace
```
# kubectl get ns
```

## Criar parta no vscode rais chamada: airflow



### Installing the Chart

https://airflow.apache.org/docs/helm-chart/stable/index.html

helm upgrade --install airflow apache-airflow/airflow --namespace airflow2 --create-namespace

```
$ helm repo add apache-airflow https://airflow.apache.org
$ helm show values apache-airflow/airflow >> airflow8/custom_values.yaml

$ helm install airflow apache-airflow/airflow \
    -f airflow8/custom_values.yaml \
    -n airflow8 \
    --create-namespace \
    --version 1.7.0 \
    --timeout 5m \
    --debug

$ helm upgrade --install airflow apache-airflow/airflow --namespace airflow8 --create-namespace
```

helm show values apache-airflow/airflow >> airflow8/custom_values.yaml


helm uninstall airflow --namespace airflow

### Configurar custom_values.yaml, alterar linhas

**Versão das tags**
```
53     airflowVersion: "2.3.0"
57     defaultAirflowTag: "2.3.0"
```

**Melhor executor para kubernets**
Vai usar a estrutura do kubernetes para subir tarefas de maneira dinamica
```
235    executor: "KubernetesExecutor"
```


**Sets variaveis de ambientes**

Para ter um log otimizado

```
244    env:
        - name: AIRFLOW__LOGGING__REMOTE_LOGGING
          value: 'True'
        - name: AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER # endereco de algum lugar no s3
          value: 's3://pucminas-log/log/'
        - name: AIRFLOW__LOGGING__REMOTE_LOG_CONN_ID # criar conexao pra autenticar no aws, my_aws eh o nome da conexao
          value: 'my_aws'
```

**Create initial user.**

```      
 951    defaultUser:
            enabled: true
            role: Admin
            username: kelly.lyra
            email: kellylyra@gmail.com
            firstName: Kelly
            lastName: Lyra
            password: admin
```
## service, altera para ip publico

```
982     service:
            type: LoadBalancer 
```
## redis, usado apena no executor celoro
```
1503    redis
            enable: false

```

## IMPORTANTE, git sync
Vincula o airflow a um repositorio git.

```
# Git sync
1777    gitSync:
            # habilitar
            enabled: true 
            # repositorio publico na conta pessoal
            repo: https://github.com/kellylyra/pos_kubectl.git
            
```

# Instalar hell no airflow
Comecar o deployment do airflow, comeca a instalacao no cluster kubernetes
```
$ git config --global user.name "kellylyra"
$ git config --global user.email kellylyra@gmail.com
```


```
$ helm install airflow apache-airflow/airflow -f airflow7/custom_values.yaml -n airflow7 --debug --dry-run

helm upgrade airflow apache-airflow/airflow --namespace airflow7
```

```
$ helm delete airflow --namespace airflow
```


helm install airflow2 apache-airflow2/airflow -f airflow2/custom_values.yaml -n airflow2 --debug

```
$ astro dev init
$ astro dev start
```
listar se esta rodando››
```
$ kubectl get pods -n airflow8
```

listar os clusters
```
$ kubectl get svc -n airflow8
```

# pagina web
```
$ kubectl get pods -n airflow8
$ kubectl get svc -n airflow8
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
$ kubectl get pvc -n airflow2
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

## EC2
### criar ke pair

### criar security group
 ass regla permitindo SSH

# programacao
- apos desenvolver o codigo, copiar arquivo .py para  aws

- adicionar no git hub

# rodar dag no airflow

## logs aws
download logs
```
$ ssh -i ney-pucminas-testes.pem xpto.compute-1.amazonaws.com
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
$ helm delete airflow -n airflow
```

## listar status dos recursos
garantir que esta sendo removido

- loadbalance
```
$ kubectl get svc -n airflow
```
caso nao remova, fazer manualmente
```
$ kubectl delete svc --all -n airflow
```

- pvc
```
$ kubectl get pvc -n airflow
```
caso nao remova, fazer manualmente
```
$ kubectl delete pvc --all -n airflow
```

# Deletar as stacks no CloudFormation

```
$ eksctl delete cluster --region=us-east-1 --name=kubea3datatrabalhokelly2
```
