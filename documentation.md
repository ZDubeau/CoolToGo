# Conception technique

## Structure de la base de données

La base de données du Back-End est constitué de **18** tables (voir annexe). La table pour gérer les accès au « Front-End » du « Back-End » :
 - administrators
 
 Les tables pour gérer les informations de projets, sélections et lieux :
 - project
 - selection
 - data_from_apidae

Les tables pour gérer les informations d’extractions par selection :
 - selection_extraction
 
 Les tables pour gérer les catégories, les profils usagers, les niveaux de fraîcheur :
 - category
 - profil
 - freshness
 
 La table pour gérer les « éléments de références » d’apidae-tourisme :
- elementreference

Les tables pour gérer les liens entre category, profil et elementreference :
- eltref_category
- eltref_profil

Les tables pour gérer les liens entre category, profil et selection :
- selection_category
- selection_profils_usager

Les tables pour gérer les liens entre category, profil et data_from_apidae suite
au traitement de transformation :
- category_apidae
- profil_apidae

Les tables pour gérer les liens entre category, profil et data_from_apidae en cas d’édition manuelle :
- category_apidae_edited
- profil_apidae_edited

La table pour gérer les informations des messages :
- message

La base de données a été optimisée avec l’utilisation de clef primaire dans toutes les tables et de « references » dès que c’était possible.

Pour gérer la connexion à la base de données j’ai choisi de créer une classe qui va lire les informations stockées dans les variables d’environnements, créer une connexion à la base de données dans le constructeur et j’ai également créé un destructeur afin d’éviter les problèmes d’un trop grand nombre de connexions actives à la base de données. Si en local je n’ai pas eu ce problème, il est apparu assez rapidement sur Heroku en raison d’une limitation à *20 connexions simultanées* à Heroku Postgres.

## Un « Front-End » pour le « Back-End »

Cet outil s’adressant à des non-informaticien, il était nécessaire d’avoir une interface intuitive qui s’affranchisse d’une utilisation en ligne de commande.
J’ai décidé de continuer de gérer l’interface avec le module [Flask](https://flask.palletsprojects.com/en/1.1.x/) car j’avais débuté ainsi dans mon projet court et j’avais pu noter un fort intérêt des « clients » pour cette approche. Afin de gérer les différentes saisies j’ai mis en place des formulaires dont certains avec des contrôles avancés. Pour gérer l’affichage des différentes tables, j’ai utilisé le module [Datatable](https://datatables.net/) et la mise en forme grâce à du javascript. 
Enfin, j’ai également géré l’import d’un fichier Excel (au format xls) pour les « éléments de références » d’apidae-tourisme.
Ces différentes actions m’ont permis :
- De présenter des données utilisables immédiatement
- De gérer différents types d’entrée de données via :
	1. Une API
	2. Un formulaire
	3. Un fichier
- De faire une application évolutive et sans données figés en dur dans le code

## Gestion de tâches asynchrones et multithreading

Afin de gérer le les extractions sans pénaliser l’accès au « Back-End », j’ai choisi de les lancer de manière asynchrone en utilisant le module [Celery](https://docs.celeryproject.org/en/stable/) de Python. Ce module permet de gérer une file d’attente de tâche à effectuer qui seront effectués par un processus différent de celui de permettant l’affichage dans un navigateur. Pour fonctionner *Celery* nécessite un agent de message (*brokers*). J’ai choisi d’utiliser [Redis Cloud](https://elements.heroku.com/addons/rediscloud) car il permet d’avoir un plus grand nombre de connections dans sa version gratuite. Il s’agit de l’une des limitations les plus difficiles que j’ai eu à lever dans le cadre de ce projet car je n’ai pas trouvé beaucoup de moyens pour limiter ce nombre de connections.
Afin d’accélérer, les temps de traitement, j’ai également décidé de mettre en place du multithreading pour paralléliser les extractions des données de lieux. Cette optimisation permet de garantir une extraction et un traitement des données en quelques minutes pour plusieurs centaines de lieux.
Ces deux optimisations ont été nécessaires pour garantir un bon fonctionnement sur Heroku car sans tâche asynchrone Heroku interrompt le traitement au bout de *30 secondes*.
Le multithreading permettant de diminuer les temps d’exécutions également. Cependant, j’ai également dû me pencher sur des problématiques d’un trop grand nombre de connexions ouvertes vers la base de données Heroku Postgres et d’un trop grand nombre de clients connectés au service Redis. Dans l’état actuel des choses le service est fonctionnel mais une optimisation serait judicieuse ou alors une migration vers un environnement n’ayant pas ces contraintes.

## Utilisation de ressources de résolution d’adresses

Lors de la récupération des informations de lieux à partir d’apidae-tourisme il est possible que les informations de longitude et latitude pour le lieu soient absente. De même, lors de saisie manuelle, il est nécessaire de les calculer à partir de l’adresse saisie.
Pour déterminer ces informations, j’ai utilisé le service [BANFrance](https://www.data.gouv.fr/fr/datasets/base-adresse-nationale/) avec le module [GeoPy](https://geopy.readthedocs.io/en/stable/) de Python. J’ai intégré la notion de temporisation dans les appels au service et de gestion des erreurs afin de limiter les anomalies.
Ce fut un bon exercice, afin de mieux comprendre l’appel à des API et comment gérer des temps d’attentes.
Sur l’échantillon de données extraites, plusieurs dizaines d’adresses sont résolues et pour toutes nous pouvons trouver une longitude et une latitude.

## Mise en place et test de l’API du « Back-End »

Afin de communiquer efficacement entre le « Front-End » et le « Back-End » nous avons décidé de mettre en place une API. Adam Roberts a fourni les schémas d’appel qu’il souhaitait mettre en place et ensuite je les ai intégré dans le « Back-End » en utilisant Flask.
Le principe est simple soit c’est l’appel d’une route avec la méthode « GET » soit c’est l’appel d’une route avec la méthode « POST » avec un json pour passer les paramètres d’entrées. Dans tous les cas un json est généré pour ensuite être intégré dans le « Front-End ».
Autant pour tester l’appel d’une page par une méthode « GET » c’est très facile et j’ai même intégré une page pour visualiser ces infos sur le « Front-End » du « Back-End » autant pour tester avec la méthode « POST » avec les paramètres passés en json, j’étais un peu perdue. Heureusement Adam m’a présenté l’outil [Postman](https://www.postman.com/) qui permet de simuler de tels appels. J’ai donc pu tester cette fonctionnalité avant de la déployer.

## Planification de tâches

Pour gérer la planification des tâches j’aurai pu utiliser le module Celery mais j’ai choisi d’utiliser [Heroku Scheduler](https://elements.heroku.com/addons/scheduler) et de créer une tâche planifiée qui va s’exécuter toutes les nuits vers 1h AM UTC.
Les principes d’extractions qui ont été mis en place font que le système va mettre à jour les données sans changer les éditions manuelles qui auraient pu être faites. Les seules données qui seront supprimés sont celles qui ne sont pas extraites d’apidae-tourisme.

## Un module de [log](https://fr.wikipedia.org/wiki/Historique_(informatique))

Tant dans une phase de développement que dans une phase d’exécution, il est important d’avoir une trace des événements qui se produisent. En local, les instances Flask et Celery s’exécutent sur des processus différents. Sur Heroku, c’est similaire auquel vient s’ajouter la notion de [dynos](https://www.heroku.com/dynos).
C’est pourquoi j’ai décidé d’utiliser un module de log pour historiser les différents événements qui se produisent dans l’application indépendamment du processus ou du dynos sur lequel ils apparaissent. J’ai défini plusieurs « tag » suivant qu’il s’agit d’une erreur, d’une information, d’une alerte, …
Ce module m’a été bien utile pour mieux comprendre les erreurs et surtout les limitations de la plateforme Heroku dans sa version gratuite mais également de certains services. Avant d’utiliser BANFrance, j’ai utilisé [Nominatim](https://nominatim.openstreetmap.org/) qui était plus pénalisant en termes d’attente entre deux requêtes et moins performant dans certains cas.
Ce module peut être réutilisé facilement dans un autre projet, dans un autre contexte.

# Process

Dans le cadre de ce projet nous avons utilisé une méthodologie [AGILE](https://fr.wikipedia.org/wiki/M%C3%A9thode_agile) avec les notions de « [Product Backlog](https://www.scrum.org/resources/what-is-a-product-backlog) », de « [Stand-Up Meeting](https://en.wikipedia.org/wiki/Stand-up_meeting) » et de « [Sprint](https://fr.wikipedia.org/wiki/Sprint_(d%C3%A9veloppement_logiciel)) ».
Le projet a été traité en **4** « Sprint » :
- Le premier « Sprint » correspondant au projet court que j’ai pu faire dans la phase des projets en groupe et qui en raison du confinement lié à la pandémie Covid-19 s’est transformé en un projet solo.
- Les 3 autres « Sprint » ont été réalisés dans le cadre du stage de 8 semaines.

## Gestion du « Product Backlog »

Etant la seule développeuse, un [Trello](https://trello.com/fr) (voir annexe) a été mis en place pour visualiser les tâches et leur avancement. Elsa Batelier a joué le rôle du « Product Owner » et elle a alimenté le « Product Backlog » tout au long du projet.
J’ai mis à jour les tâches en fonctions de leur avancement et nous faisions le point régulièrement.

### Sprint 0 : extraction des données et transformations (projet de 3 semaines)

Ce premier sprint a eu lieu entre mars et avril 2020. J’ai pu y mettre en place les fonctionnalités
- D’extractions des sélections pour un projet
- Des lieux pour une sélection
- Le multithreading
- L’interface utilisateur administrateur

Par manque de temps, je n’avais pas pu travailler sur l’automatisation de la définition des catégories, des profils utilisateurs ou du niveau de fraicheur.

### Sprint 1 : automatisation de l’association des catégories et des profils usagers

Ce premier sprint du stage a eu lieu du 3 Juin au 30 Juin 2020. 
L’une des premières actions fût de comprendre la notion d’éléments de références.
Comment ils sont définis dans la base de données apidae-tourisme et comment ils sont utilisés dans les lieux.
Ensuite, j’ai défini les tables des catégories, des profils et du niveau de fraicheur et les relations qu’elles ont avec les « éléments de références ». Enfin, j’ai fait évoluer le module transformation afin de prendre en compte ces éléments dans la détermination des catégories et du profil d’usager pour un lieu.
J’ai fait en sorte que l’administrateur, ait totalement la main sur l’association des « éléments de références » aux profils usagers et aux catégories afin de rien « graver dan le marbre » du code et ainsi avoir un traitement le plus évolutif possible.

### Sprint 2 : mise en place de l’API
Ce deuxième sprint du stage a eu lieu du 1er Juillet au 15 Juillet 2020.
Lors de ce « Sprint », j’ai dû analyser le format attendu par Adam Roberts pour le « Front-End » de CoolToGo. J’ai ensuite travaillé sur le format des fichiers json qui doivent être renvoyés.
J’ai testé le tout avec le logiciel Postman qu’ai dû apprivoiser car c’est la première fois que j’en utilisais un de ce type. Après quelques essais, j’ai pu valider que je renvoyais un fichier json au format similaire au retour attendu.
Ces rendus ont permis de mettre à jour le site CoolToGo.

### Sprint 3 : optimisation et documentation

Ce troisième sprint du stage a eu lieu du 16 Juillet au 3 Août 2020.
Au cours de ce « Sprint », j’ai essentiellement travaillé sur de l’optimisation du code, de la simplification et de la documentation.
L’objectif étant de supprimer le code non utile, de documenter au maximum :
- Par la mise en place de commentaires dans le code quand c’était nécessaire.
- La création d’une aide utilisateur accessible directement sur le « Front-End » du « Back-End ».
- L’écriture de ce rapport de stage que je souhaite ajouter dans la partie documentation accessible sur le « Front-End » du « Back-End ».

### Développement en suivant la philosophie [CI/CD](https://en.wikipedia.org/wiki/CI/CD)

Tout au long du projet j’ai développé en local tout en publiant très régulièrement sur *GitLab* pour éviter les pertes de données et également pour valider les choix techniques sur Heroku.
*l'équipe Turbine* et *Adam Roberts* ont accès à la plateforme Heroku et à GitLab pour suivre ces déploiements.
L’une des difficultés que j’ai rencontrées, consistait à la mise à jour de la base de données jusqu’à ce que je découvre [pgAdmin](https://www.pgadmin.org/). Cet utilitaire à simplifié la mise en place des nouvelles versions lorsqu’elles étaient assorties d’une évolution de la base de données.
