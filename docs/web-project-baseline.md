# Web Project Baseline

La skill web-project-baseline définit une revue de complétude pour les projets web publics substantiels.

## Pourquoi

Amplio Web montre que la complétude de production est distribuée dans de nombreux petits systèmes :
- routes et pages légales ;
- header/footer/nav partagés ;
- responsive ;
- clavier/accessibilité ;
- contenu data-driven ;
- cycle de formulaire ;
- storage/tracking ;
- SEO ;
- assets et ressources tierces ;
- motion et 3D avec fallback ;
- états d'erreur et de repli ;
- hosting/security ;
- browser QA ;
- documentation et preuves.

Le but de la baseline est de rendre ces responsabilités visibles dès le démarrage et de les vérifier avant la release.

## Observations Amplio réutilisables

Dans sudomarc/amplio-web, on observe notamment :
- plusieurs pages publiques ;
- partials header/footer ;
- services.json et projects.json ;
- validation des données dynamiques ;
- continuité sélection de service → contact ;
- formulaire avec validation, état pending, succès/erreur et focus ;
- skip link, navigation active, menu mobile ;
- responsive smoke testing ;
- reduced-motion ;
- Three.js facultatif avec fallback WebGL et pause hors viewport ;
- pages privacy/legal ;
- robots.txt, Open Graph et favicon ;
- configuration Netlify ;
- roadmap et documentation de vérification.

## Correction importante : cookies

Amplio ne possède pas de cookie consent manager.

Son legal note indique qu'aucun cookie n'est déposé et mémorise la fermeture avec localStorage. Ce mécanisme est une notice informative, pas un système universel de consentement aux cookies.

Donc la baseline n'exige pas de cookie banner par défaut. Elle exige un inventaire du stockage et du tracking, puis un vrai consent system seulement si le comportement réel du projet et les règles applicables l'exigent.

## Conflit de preuve observé

Le code source d'Amplio contient des ressources externes, notamment Google Fonts, une librairie Three.js CDN et des images distantes. Une partie de la documentation de vérification indiquait pourtant l'absence de ressources externes.

Cette classe de conflit doit être gérée par les preuves runtime et signalée comme CONFLICT/UNKNOWN, pas résolue par une supposition.

## Résultat attendu

Pour tout nouveau projet web public, créer ou planifier les équivalents fonctionnels de ces responsabilités, implémenter uniquement les capacités applicables et maintenir leur statut jusqu'à la vérification de release.
