class transformation():
    """First step for retrieve Data from Apidae"""

    def __init__(self, request_json, list_of_special_element=[]):
        self.__request_json = request_json
        self.__dict_id = {}
        self.__list_elements_de_references = []
        self.__special_elements = list_of_special_element
        self.__special_elements_descriptions = dict()
        for element in self.__special_elements:
            self.__special_elements_descriptions[element] = ""

    def __general_information(self):

        self.__dict_id['id_selection'] = None
        self.__dict_id['type_apidae'] = None
        self.__dict_id['titre'] = None

        # selection id
        if 'id' in self.__request_json:
            self.__dict_id['id_apidae'] = self.__request_json['id']
        # type Apidae
        if 'type' in self.__request_json:
            self.__dict_id['type_apidae'] = self.__request_json['type']
        # titre
        if 'nom' in self.__request_json:
            if 'libelleFr' in self.__request_json['nom']:
                self.__dict_id['titre'] = self.__request_json['nom']['libelleFr']

    def __benefit(self):

        self.__dict_id['tourisme_adapte'] = None
        self.__dict_id['animaux_acceptes'] = None

        # tourisme_adapte
        if 'prestations' in self.__request_json:
            if 'tourismesAdaptes' in self.__request_json['prestations']:
                if 'libelleFr' in self.__request_json['prestations']['tourismesAdaptes'][0]:
                    self.__dict_id['tourisme_adapte'] = self.__request_json['prestations']['tourismesAdaptes'][0]['libelleFr']
        # Animaux_acceptes
        if 'prestations' in self.__request_json:
            if 'animauxAcceptes' in self.__request_json['prestations']:
                self.__dict_id['animaux_acceptes'] = self.__request_json['prestations']['animauxAcceptes']

    def __environment(self):

        self.__dict_id['environnement'] = None

        if 'localisation' in self.__request_json:
            if 'environnements' in self.__request_json['localisation']:
                Environnement = ""
                first = True
                for value in self.__request_json['localisation']['environnements']:
                    if 'libelleFr' in value:
                        if first:
                            Environnement += value['libelleFr']
                            first = False
                        else:
                            Environnement += ", " + value['libelleFr']
                self.__dict_id['environnement'] = Environnement

    def __equipment(self):

        self.__dict_id['equipement'] = None

        if 'prestations' in self.__request_json:
            if 'equipements' in self.__request_json['prestations']:
                Equipement = ""
                first = True
                for value in self.__request_json['prestations']['equipements']:
                    if 'libelleFr' in value:
                        if first:
                            Equipement += value['libelleFr']
                            first = False
                        else:
                            Equipement += ", " + value['libelleFr']
                self.__dict_id['equipement'] = Equipement

    def __image(self):

        self.__dict_id['image'] = None

        if 'illustrations' in self.__request_json:
            if 'traductionFichiers' in self.__request_json['illustrations'][0]:
                if 'url' in self.__request_json['illustrations'][0]['traductionFichiers'][0]:
                    self.__dict_id['image'] = self.__request_json['illustrations'][0]['traductionFichiers'][0]['url']

    def __paying(self):

        self.__dict_id['payant'] = None

        if 'descriptionTarif' in self.__request_json:
            if 'gratuit' in self.__request_json['descriptionTarif']:
                if self.__request_json['descriptionTarif']['gratuit'] == False:
                    self.__dict_id['payant'] = 'Oui'
                else:
                    self.__dict_id['payant'] = 'Non'

    def __public(self):

        self.__dict_id['publics'] = None

        if 'prestations' in self.__request_json:
            if 'typesClientele' in self.__request_json['prestations']:
                Public = ""
                first = True
                for value in self.__request_json['prestations']['typesClientele']:
                    if 'libelleFr' in value:
                        if first:
                            Public += value['libelleFr']
                            first = False
                        else:
                            Public += ", " + value['libelleFr']
                self.__dict_id['publics'] = Public

    def __service(self):

        self.__dict_id['services'] = None

        if 'prestations' in self.__request_json:
            if 'services' in self.__request_json['prestations']:
                Service = ""
                first = True
                for value in self.__request_json['prestations']['services']:
                    if 'libelleFr' in value:
                        if first:
                            Service += value['libelleFr']
                            first = False
                        else:
                            Service += ", " + value['libelleFr']
                self.__dict_id['services'] = Service

    def __opening(self):

        self.__dict_id['ouverture'] = None

        if 'ouverture' in self.__request_json:
            if 'periodeEnClair' in self.__request_json['ouverture']:
                if 'libelleFr' in self.__request_json['ouverture']['periodeEnClair']:
                    self.__dict_id['ouverture'] = self.__request_json['ouverture']['periodeEnClair']['libelleFr']

    def __period(self):

        self.__dict_id['periode'] = None

        if 'ouverture' in self.__request_json:
            if 'indicationsPeriode' in self.__request_json['ouverture']:
                Opening = ""
                first = True
                for element in self.__request_json['ouverture']['indicationsPeriode']:
                    if 'libelleFr' in element:
                        if first:
                            Opening += element['libelleFr']
                            first = False
                        else:
                            Opening += ", " + element['libelleFr']
                self.__dict_id['periode'] = Opening

    def __activity(self):

        self.__dict_id['activites'] = None

        if 'prestations' in self.__request_json:
            if 'activites' in self.__request_json['prestations']:
                Activity = ''
                first = True
                for value in self.__request_json['prestations']['activites']:
                    if 'libelleFr' in value:
                        if first:
                            Activity += value['libelleFr']
                            first = False
                        else:
                            Activity += ', ' + value['libelleFr']
                self.__dict_id['activites'] = Activity

    def __description(self):

        self.__dict_id['description_courte'] = None
        self.__dict_id['description_detaillee'] = None

        if 'presentation' in self.__request_json:
            # description courte
            if 'descriptifCourt' in self.__request_json['presentation']:
                if 'libelleFr' in self.__request_json['presentation']['descriptifCourt']:
                    self.__dict_id['description_courte'] = self.__request_json['presentation']['descriptifCourt']['libelleFr']
            # description détaillée
            if 'descriptifDetaille' in self.__request_json['presentation']:
                if 'libelleFr' in self.__request_json['presentation']['descriptifDetaille']:
                    self.__dict_id['description_detaillee'] = self.__request_json['presentation']['descriptifDetaille']['libelleFr']

    def __geolocation(self):

        self.__dict_id['adresse1'] = None
        self.__dict_id['adresse2'] = None
        self.__dict_id['ville'] = None
        self.__dict_id['code_postal'] = None
        self.__dict_id['altitude'] = None
        self.__dict_id['longitude'] = None
        self.__dict_id['latitude'] = None

        if 'localisation' in self.__request_json:
            # latitude, longitude
            if 'geolocalisation' in self.__request_json['localisation']:
                if 'geoJson' in self.__request_json['localisation']['geolocalisation']:
                    if 'coordinates' in self.__request_json['localisation']['geolocalisation']['geoJson']:
                        self.__dict_id['longitude'] = self.__request_json['localisation']['geolocalisation']['geoJson']['coordinates'][0]
                        self.__dict_id['latitude'] = self.__request_json['localisation']['geolocalisation']['geoJson']['coordinates'][1]
            # adresse1, adresse2
            if 'adresse' in self.__request_json['localisation']:
                if 'adresse1' in self.__request_json['localisation']['adresse']:
                    self.__dict_id['adresse1'] = self.__request_json['localisation']['adresse']['adresse1']
                if 'adresse2' in self.__request_json['localisation']['adresse']:
                    self.__dict_id['adresse2'] = self.__request_json['localisation']['adresse']['adresse2']
            # ville
            if 'adresse' in self.__request_json['localisation']:
                if 'commune' in self.__request_json['localisation']['adresse']:
                    if 'codePostal' in self.__request_json['localisation']['adresse']:
                        self.__dict_id['code_postal'] = self.__request_json['localisation']['adresse']['codePostal']
                        if 'nom' in self.__request_json['localisation']['adresse']['commune']:
                            self.__dict_id['ville'] = self.__request_json['localisation']['adresse']['commune']['nom']
            # altitude
            if self.__dict_id['altitude'] is None:
                if 'informations' in self.__request_json:
                    if 'structureGestion' in self.__request_json['informations']:
                        if 'geolocalisation' in self.__request_json['informations']['structureGestion']:
                            if 'altitude' in self.__request_json['informations']['structureGestion']['geolocalisation']:
                                self.__dict_id['altitude'] = self.__request_json['informations'][
                                    'structureGestion']['geolocalisation']['altitude']
            # latitude, longitude
            if 'localisation' in self.__request_json:
                if 'geolocalisation' in self.__request_json['localisation']:
                    if 'geoJson' in self.__request_json['localisation']['geolocalisation']:
                        if 'coordinates' in self.__request_json['localisation']['geolocalisation']['geoJson']:
                            self.__dict_id['longitude'] = self.__request_json['localisation']['geolocalisation']['geoJson']['coordinates'][0]
                            self.__dict_id['latitude'] = self.__request_json['localisation']['geolocalisation']['geoJson']['coordinates'][1]

    def __typology(self):

        self.__dict_id['typologie'] = None
        if 'presentation' in self.__request_json:
            if 'typologiesPromoSitra' in self.__request_json['presentation']:
                typology = ""
                first = True
                for value in self.__request_json['presentation']['typologiesPromoSitra']:
                    if 'libelleFr' in value:
                        if first:
                            typology += value['libelleFr']
                            first = False
                        else:
                            typology += ", " + value['libelleFr']
                self.__dict_id['typologie'] = typology

    def __find_element_reference_in_json(self, jsonfile):
        list_element_reference = []
        for key in jsonfile:
            intermediatejson = jsonfile[key]
            if isinstance(intermediatejson, dict):
                list_element_reference.extend(
                    self.__find_element_reference_in_json(intermediatejson))
            elif isinstance(intermediatejson, list):
                for element in intermediatejson:
                    if isinstance(element, dict):
                        list_element_reference.extend(
                            self.__find_element_reference_in_json(element))
            if key == 'elementReferenceType':
                list_element_reference.append(jsonfile['id'])
        return sorted(list(dict.fromkeys(list_element_reference)))

    def __identify_all_elements_de_reference(self):
        self.__list_elements_de_references = self.__find_element_reference_in_json(
            self.__request_json)

    def __identify_special_elements_descriptions(self, jsonfile, jsonfileparent):
        try:
            for key in jsonfile:
                intermediatejson = jsonfile[key]
                if isinstance(intermediatejson, dict):
                    self.__identify_special_elements_descriptions(
                        intermediatejson, jsonfile)
                elif isinstance(intermediatejson, list):
                    for element in intermediatejson:
                        if isinstance(element, dict):
                            self.__identify_special_elements_descriptions(
                                element, jsonfile)
                if key == 'elementReferenceType' and jsonfile['id'] in self.__special_elements:
                    self.__special_elements_descriptions[jsonfile['id']
                                                         ] += " *********** " + jsonfileparent['description']['libelleFr']
        except Exception:
            pass
            #print(jsonfile, jsonfileparent)

    def __identify_all_special_elements_descriptions(self):
        for key in self.__request_json:
            intermediatejson = self.__request_json[key]
            if isinstance(intermediatejson, dict):
                self.__identify_special_elements_descriptions(
                    intermediatejson, self.__request_json)

    def Execute(self):
        self.__general_information()
        self.__benefit()
        self.__environment()
        self.__description()
        self.__typology()
        self.__geolocation()
        self.__paying()
        self.__period()
        self.__activity()
        self.__opening()
        self.__service()
        self.__equipment()
        self.__public()
        self.__image()
        self.__identify_all_elements_de_reference()
        self.__identify_all_special_elements_descriptions()
        if 'descriptifsThematises' in self.__request_json['presentation']:
            nb_description_thematise = len(
                self.__request_json['presentation']['descriptifsThematises'])
            if nb_description_thematise > 2:
                print(self.__dict_id['id_apidae'], nb_description_thematise)

    def dict_id(self):
        return self.__dict_id

    def list_elements_de_references(self):
        return self.__list_elements_de_references

    def special_elements_descriptions(self):
        return self.__special_elements_descriptions
