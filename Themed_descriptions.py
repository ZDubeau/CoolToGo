class thematisee():

    def __init__(self, request_json):
        self.__request_json = request_json
        self.__dict_id = {}

    def __descriptifThematisee(self):
        self.__dict_id['Bons_plans'] = None
    self.__dict_id['Dispositions_spéciales'] = None
    if 'presentation' in self.__request_json:
        if 'descriptifsThematises' in self.__request_json['presentation']:
            firstBP = True
            firstDS = True
            for value in self.__request_json['presentation']['descriptifsThematises']:
                if 'theme' in value:
                    if 'libelleFr' in value['theme']:
                        if value['theme']['libelleFr'] == 'Bons plans':
                            if firstBP:
                                self.__dict_id['Bons_plans'] = value['description']['libelleFr']
                                firstBP = False
                            else:
                                self.__dict_id['Bons_plans'] += " ///// " + \
                                    value['description']['libelleFr']
                        elif value['theme']['libelleFr'] == 'Dispositions spéciales COVID 19':
                            if firstDS:
                                self.__dict_id['Dispositions_spéciales'] = value['description']['libelleFr']
                                first = False
                            else:
                                self.__dict_id['Dispositions_spéciales'] += " ///// " + \
                                    value['description']['libelleFr']

    def descriptif_thematise(self):
        self.__descriptifThematisee()

    def dict_id(self):
        return self.__dict_id
