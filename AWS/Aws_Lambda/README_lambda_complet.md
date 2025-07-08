# AWS Lambda : Plus d’efficacité, Moins de Coûts 💡

## 🚀 Objectif du Projet

Automatiser l’arrêt et le démarrage de vos instances **EC2** avec **AWS Lambda** et **Amazon EventBridge**, pour optimiser les coûts d'infrastructure.

---

## 🧠 Qu'est-ce que AWS Lambda ?

AWS Lambda est un **service de calcul serverless** qui exécute du code en réponse à des événements, sans nécessiter la gestion de serveurs.

- ⚙️ Événements déclencheurs : S3, DynamoDB, SNS, SQS, API Gateway, etc.
- 💰 Paiement uniquement à l'exécution.
- 🛠️ Support de plusieurs langages : Python, Node.js, Java, Go, etc.
- 🔧 Déploiement via AWS Console, CLI, ou SDK.

---

## 🔍 Fonctionnement

1. **Écriture du code** :
   - Dans l'IDE en ligne d'AWS.
   - Ou via un fichier ZIP ou image Docker.

2. **Configuration du déclencheur** :
   - Planifié (EventBridge, ex: toutes les nuits à minuit).
   - Basé sur un événement AWS (ex: ajout dans un S3).

3. **Définition des permissions (IAM)** :
   - Rôle IAM permettant l’accès aux services nécessaires (EC2, CloudWatch, etc.).

4. **Déploiement & Exécution** :
   - AWS alloue les ressources, exécute le code de manière isolée, puis les libère.

---

## 🧩 Particularités de Lambda

- 📈 Intégration automatique avec CloudWatch.
- 🔁 Haute disponibilité et tolérance aux pannes intégrées.
- ❌ Pas besoin de Load Balancer ou de backups manuels.

---

## 💼 Cas Pratique : Démarrer et Arrêter des Instances EC2 Automatiquement

### 🎯 Objectif :
Réduire la facture AWS en arrêtant les instances EC2 la nuit et les redémarrant le matin.

### Étapes de mise en œuvre :

#### ✅ Étape 1 : Créer un rôle IAM
- Permissions EC2 + CloudWatch.
- Exemple : démarrer/arrêter une instance, écrire dans CloudWatch.

#### ✅ Étape 2 : Créer une fonction Lambda `demarrage`
- Runtime : Python 3.13
- Rôle IAM : `Lambda_Execution_Role`

#### ✅ Étape 3 : Déclencheur avec EventBridge
- Type : Schedule expression
- Expression : `cron(0 5 * * ? *)` (5h GMT)

#### ✅ Étape 4 : Ajouter et déployer le code Python
- Remplacer :
  - `'us-east-1'` par ta région (ex : `'eu-west-1'`)
  - `'i-0123456789abcdef0'` par ton ID d’instance EC2

#### ✅ Étape 5 : Vérification
- Utiliser CloudWatch pour consulter les logs
- Vérifier l’état des instances dans la console EC2

---

## 🛑 Fonction Lambda pour Arrêter les Instances

- Nouvelle fonction : `arreter`
- Même rôle IAM (`Lambda_Execution_Role`)
- Déclencheur via EventBridge : `cron(0 22 * * ? *)` (22h GMT)
- Code Python adapté avec `ec2.stop_instances()`

---

## ✅ Résultat Final

| Fonction        | Heure d'exécution | Action               |
|-----------------|-------------------|----------------------|
| `demarrage`     | 05h GMT           | Démarre EC2          |
| `arreter`       | 22h GMT           | Arrête EC2           |

---

## 📸 Architecture

*(Tu peux ici ajouter une image de l’architecture ou un schéma si disponible)*

---

## 📎 Liens utiles

- [Documentation AWS Lambda](https://docs.aws.amazon.com/fr_fr/lambda/latest/dg/welcome.html)
- [Documentation EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/what-is-amazon-eventbridge.html)

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
