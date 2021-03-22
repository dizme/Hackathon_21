# Hackathon_21

## OBIETTIVO
Individuare idee originali e realizzare soluzioni innovative sul tema dell’**identità digitale decentralizzata** (*self sovereign identity*).

*Grazie ad HACKATHON_21, Dizme Foundation vuole promuovere lo sviluppo di un nuovo modello di identità che ci consenta di ottenere un reale controllo sui nostri dati e proteggere la nostra privacy.*

## A CHI E’ RIVOLTO? 
-	**Startup/PMI innovative**: interessate ad integrare il tema della self sovereign identity all’iterno dei loro servizi e/o prodotti
-	**Talenti - innovatori, singoli o in gruppo** – interessati a sviluppare e proporre idee sul tema della self sovereign identity
- **LegalTech** – studi legali e singoli professionisti - esperti di digital compliance che sceglieranno uno dei casi d’uso esistenti per sviluppare uno studio di fattibilità riguardo i vincoli normativi

## LE SFIDE 
Definite sui ruoli di identità di una persona o un’organizzazione

- Challenge G2C | Government to **Citizen** – soluzioni per il Cittadino che si relaziona con la Pubblica Amministrazione
- Challenge B2C | Business to **Consumer** – soluzioni per il Consumatore che accede a servizi retail, finanziari, assicurativi, utility, telco  
- Challenge B2E | Business to **Employee** – soluzioni per lo studente che si relaziona con enti di istruzione e formazione o per il lavoratore che interagisce con l’ecosistema aziendale
- Challenge B2B | Business to **Business** – soluzioni per il legale rappresentate che opera in nome e per conto di una persona giuridica
- Challenge B2T | Business to **Things** – soluzioni per il controllo e la gestione di asset digitali e non

![Challenge](images/hackathonchallenge.png)

### SCENARI D'USO

|Citizen G2C|Consumer B2C|Learner/Worker B2E |Asset owner B2T|Legal Identity owner B2B
|-----------|------------|-------------------|---------------|------------------------
|Emergenza Covid19: Certificazione esito test; Certificazione stato vaccinale; Consenso informato; Verifica anonima di esiti/stati|Onboarding web via Dizme wallet |Zero Trust security: accesso alle risorse aziendali in modalità SSI|Gestione manutenzioni e ispezioni: Certificazione tecnici abilitati; Certificazione data-ora e geolocalizzazione |Contract Management: contrattualizzazione digitale end-to-end
|Gare pubbliche e concorsi: trasparenza e valutazione requisiti partecipanti |Membership e loyalty program via Dizme wallet|eVoting: Gestione del voto remoto (assemblee soci, associazioni, ordini professionali) in modalità elettronica | Provisioning IOT: Certificazione proprietà; Pairing e accesso controllato |

Per maggiori dettagli relativi agli scenari d'uso i partecipanti all'hackathon possono visionare le [slide](https://teams.microsoft.com/l/file/0E7CFA45-698D-4337-9A96-C2FBC5E57ED6?tenantId=9f152cda-ffaa-4335-9465-5c1b47d649cd&fileType=pdf&objectUrl=https%3A%2F%2Fgrowitupitaly.sharepoint.com%2Fsites%2FThisismeHackathon_21%2FDocumenti%20condivisi%2FGeneral%2FKickOff%2FHackathon21%20Kickoff_final.pdf&baseUrl=https%3A%2F%2Fgrowitupitaly.sharepoint.com%2Fsites%2FThisismeHackathon_21&serviceName=teams&threadId=19:d992dd77f6984949821687c80fea0eeb@thread.tacv2&groupId=a5a7bdb4-2b08-4f14-9c50-6a1aaee22825) presentate al kickoff
 			

## LA TECNOLOGIA 
I partecipanti potranno realizzare il proprio progetto innovativo facendo leva sulle componenti dell'ecosistema Dizme e sui servizi dei Partner Tecnologici. 

![Tools](images/tools.png)

### Dizme Wallet 
Una mobile app per l'utente finale (*holder*) per il completo controllo delle proprie credenziali. Nel wallet digitale, protetto da un'autenticazione multi-fattore, le informazioni personali sono salvate sotto forma di Verifiable credential (formato standard W3C). 
> *Dizme wallet in stage environment è scaricabile nelle versioni iOS e Android.*

### Dizme API
Le API abilitanto i partecipanti ad interagire con i wallet per emettere e verificare Verifiable Credential secondo le esigenze a cui la Soluzione proposta si riferisce.
> *Dizme API sono pubblicate su [Dizme Developer Portal](https://www.dizme.io/developers)*; 
> *[Reference implementation](https://github.com/dizme/Foundation/tree/main/generic-organization)*

### Identity Verifiable Credentials
Verifiable Credentials per accelerare lo sviluppo delle Soluzioni sono disponibili all'interno del wallet per la verifica dell'identità di una persona fisica tramite selfie, liveness detection, riconoscimento documenti di identità, autenticazione SPID e autenticazione bancaria.

### InfoCert API
API di servizi InfoCert per realizzare Soluzioni che integrino processi di firma digitale avanzata (FEA) e firma digitale qualificata (FEQ). 

### Algorand Platform
Algorand mette a disposizione:
1.	Setting dei tool di sviluppo (nodo, docker sandbox, smart contract debugger, etc.);
2.	Algorand Standard Assets: proprietà e genesi di token su Algorand tramite CLI oppure SDK (Python);
3.	Algorand Smart Contracts: linguaggio TEAL, logica di sviluppo e debug sia per la versione Stateless che Stateful;
4.	SDK Python: gestione su back-end Python di creazione account, scrittura e firma transazioni, query dati in blockchain

### Fabrick API
API di integrazione con Fabrick Platform and Fabrick Pass
