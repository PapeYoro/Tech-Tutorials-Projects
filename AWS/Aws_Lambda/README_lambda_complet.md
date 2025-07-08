AWS Lambda : plus d’efficacité Moins de Couts !



Automatisez l’arrêt et le démarrage de vos instances EC2 avec Lambda et EventBridge







Qu'est-ce que AWS Lambda ?

Lambda vous permet d'exécuter du code sans provisionner ni gérer de serveurs. AWS Lambda est un service de calcul sans serveur, piloté par les événements. 

Vous créez une fonction Lambda, qui est la ressource AWS contenant le code que vous téléchargez. Vous configurez ensuite le déclenchement de la fonction Lambda, soit de manière planifiée, soit en réponse à un événement. Votre code ne s'exécute que lorsqu'il est déclenché.

Vous ne payez que pour le temps de calcul consommé ; vous n'êtes pas facturé lorsque votre code n'est pas exécuté.

Une source d'événement est un service AWS ou une application créée par un développeur qui génère des événements déclenchant l'exécution d'une fonction AWS Lambda.

Les Sources d’évènements peuvent être : Amazon S3, Amazon DynamoDB, Amazon Simple Notification Service (SNS), Amazon Simple Queue Service (Amazon SQS), Amazon API Gateway, Application Load Balancer (ALB), etc.

AWS Lambda prend en charge plusieurs langages de programmation, nous pouvons en citer : Java, Go, Powershell, Node.js, C#, Python et Ruby. De plus, elle fournit une API d’exécution qui permet aux développeurs d’utiliser d’autres langages de programmation pour créer les fonctions

Il existe plusieurs methodes pour interagir avec AWS Lamda, notamment l’utilisation de la console AWS, de l’AWS CLI (interface de ligne de commande) et des SDK AWS.

Comment AWS Lambda fonctionne ?





Ecriture du code 

Soit directement depuis l’IDE en ligne propose par AWS (dans la console Lambda),

Soit en uploadant un fichier Zip ou une image Docker contenant le code de ses dépendances.

Configurer un déclencheur : 

Il faut ensuite configurer un déclencheur (trigger) pour définir quand et comment la fonction sera exécutée 

Un évènement AWS (ex : ajout d’un fichier dans bucket S3, message dans une file SQS, etc.)

Une exécution planifiée (via Amazon Eventbridge/cloudwatch Events, par exemple toutes les nuits à minuit) 

Définition de permissions (IAM Role)

La fonction doit disposer des autorisations nécessaires pour interagir avec d’autres services AWS.

On crée pour cela un rôle IAM ( Identity Access management) contenant les permissions appropries :

Exemples : arrêter/démarrer des instances EC2, écrire dans cloudwatch logs , lire un objet S3,etc)

Déploiement et exécution

Une fois le code prêt, les permissions configurées et les déclencheurs définis :

La fonction est déployée sur AWS Lambda.

A chaque déclenchement, AWS :

Alloue automatiquement les ressources nécessaires.

Exécute le code de manière isolée.

Supprime les ressources 

Particularité d’AWS Lambda :

AWS Lambda se distingue des autres solutions d’exécution de code par plusieurs caractéristiques puissantes qui en font un choix de prédilection pour l’automatisation et les architectures modernes cloud-native

Intégration automatique avec Amazon Cloud watch 

Chaque exécution de fonction Lambda est automatiquement monitoree

Cela facilite le debug , le troubleshooting , et la surveillance continue 

Tolérance aux pannes et hautes disponibilité intégrées 

Lamba est conçu pour être résilient, scalable et redondant

 Tu n’as pas besoin de configurer un load balancer, des sauvegardes ou de la réplication manuellement 



Exemple concret : automatiser l’arrêt et le démarrage d’instances EC2 avec AWS Lambda 

Imaginons que tu souhaites réduire ta facture AWS en arrêtant tes instances EC2 pendant les heures creuses (par exemple la nuit) et les redémarrer automatiquement le matin avant le début de la journée de travail.

Grace à AWS Lambda combine a Amazon CloudWatch Events (ou Eventbridge), tu peux automatiser cette gestion sans intervention manuelle.

Déroulement de l’automatisation :

Demarrer automatique des instances EC2 :

 

Etape 1 : Creation du Role IAM 



 Role IAM créer pour permettre a Lambda de demarrer /arreter des instances EC2. Ce role inclut les permissions EC2 & CloudWatch



Etape 2 : Creation de la fonction 

Créer une nouvelle fonction Lambda dans la console :

Nom : demarrage

Runtime : Python 3.13

Rôle IAM : utiliser le nom du rôle créé précédemment (Lambda\_Execution\_Role)







 



Etape 3 : Création d’un déclencheur (Eventbridge)

Dans l’onglet Configuration, clique sur Add trigger.

Dans le menu Select a trigger, choisis EventBridge (CloudWatch Events).

Crée une nouvelle règle avec les paramètres suivants :

Rule name : everyMinute

Rule type : Schedule expression

Schedule expression : rate(1 minute)

Cette planification permet de tester rapidement la fonction. Pour un cas réel, utilise plutôt une expression CRON comme cron(0 5 * * ? *) pour demarer à 05h GMT.

Clique sur Add pour lier le déclencheur.







 

Voici l’architecture finale :





Etape 4 : Ajout de ta fonction python & déploiement



Descends à la section Code dans la console Lambda.

Clique sur lambda\_function.py pour éditer le code.

Remplace tout le code par ce qui suit :



 



Remplace :

'us-east-1' par le code de ta région (ex. 'eu-west-1' pour l’Irlande)

'i-0123456789abcdef0' par l’ID réel de ton instance EC2

Clique sur Save, puis Deploy.



Etape 5 : vérifier le fonctionnement 

Dans l’onglet Monitor de la fonction Lambda :

Vérifie le nombre d’invocations

Consulte les logs en cliquant sur View logs in CloudWatch

Assure-toi qu’il n’y a pas d’erreur (Error count = 0)

Ouvre la console Amazon EC2, et vérifie que ton instance a changé d’état :

Si elle était stopped, elle devrait passer à running dans la minute qui suit.

Clique sur le bouton Actualiser dans la console EC2 pour voir les changements en temps réel.



Fonction Lambda Pour Arrêter les instances 

Mettre le code ici 



Créer une nouvelle fonction Lambda dans la console :

Nom : Arreter

Runtime : Python 3.13

Rôle IAM : réutiliser le même Lambda\_Execution\_role (s’il a bien les permissions ec2:StopInstances)

Ajouter un déclencheur planifié via EventBridge :

Exemple CRON pour arrêter les instances à 22h du matin (GMT) chaque jour : cron (0 22 * * ? *)

Coller le code ci-dessus, remplacer :

'us-east-1' par ta région (ex : 'eu-west-1')

'i-0123456789abcdef0' par l’ID de ton instance

Enregistrer puis Déployer la fonction.



Résultat :

La fonction démarrée : Démarré toutes les instances à 5h GMT

La fonction Arrêt : éteint les instances à 22h (ou chaque minute pour test).






### Étape 4 : Ajouter ta fonction Python & Déploiement

1. Dans la console Lambda, va dans la section **Code**.
2. Clique sur `lambda_function.py` pour éditer le script.
3. Colle le code Python fourni pour arrêter ou démarrer les instances.
4. **Personnalise les éléments suivants dans le code** :
   - Remplace `'us-east-1'` par ta région AWS (ex. `'eu-west-1'` pour l’Irlande).
   - Remplace `'i-0123456789abcdef0'` par **l’ID de ton instance EC2 réelle**.
5. Clique sur **Save**, puis **Deploy**.

### ✅ Résultat attendu :

- La fonction **`demarrage`** démarre automatiquement les instances EC2 à **05h GMT**.
- La fonction **`arreter`** éteint les instances EC2 à **22h GMT** (ou chaque minute en mode test).

---

## 🔐 Politique IAM recommandée

Voici une politique IAM à attacher au rôle `Lambda_Execution_Role` pour permettre à la fonction Lambda de :

- Écrire dans **CloudWatch Logs**
- Démarrer / arrêter / décrire les instances **EC2**
- Gérer les interfaces réseau pour les appels dans un **VPC**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:StartInstances",
        "ec2:StopInstances",
        "ec2:DescribeInstances"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateNetworkInterface",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DeleteNetworkInterface"
      ],
      "Resource": "*"
    }
  ]
}
```

### 💡 Bonne pratique AWS : Séparation des politiques

Tu peux séparer cette politique en plusieurs rôles pour rester aligné avec les bonnes pratiques :

1. `AWSLambdaBasicExecutionRole` — pour écrire dans **CloudWatch Logs**
2. `AWSLambdaVPCAccessExecutionRole` — pour les appels dans un **VPC**
3. Une **politique personnalisée** avec uniquement les permissions EC2 :

```json
{
  "Effect": "Allow",
  "Action": [
    "ec2:StartInstances",
    "ec2:StopInstances",
    "ec2:DescribeInstances"
  ],
  "Resource": "*"
}
```

---

## 🤝 Trust Relationship (Relation d’approbation)

Cette configuration est nécessaire pour permettre à Lambda d'assumer le rôle IAM :

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

📌 **Où l’ajouter ?**  
- Console : dans l’onglet **Trust relationships** du rôle IAM.
- CLI : via `create-role` ou `update-assume-role-policy`.

---
