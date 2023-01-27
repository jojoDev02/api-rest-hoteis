def normalize_path_params(cidade = None,
                          estrelas_min = 0,
                          estrelas_max = 5,
                          diaria_min = 0,
                          diaria_max = 10000,
                          limit = 50, 
                          off_set = 0, **dados):
    
    if not cidade:
        return {
            'estrelas_min' : estrelas_min,
            'estrelas_max' : estrelas_max,
            'diaria_min' : diaria_min,
            'diaria_max' : diaria_max,
            'limit': limit,
            'offset': off_set
        }
    return{
        'cidade' : cidade,
        'estrelas_min' : estrelas_min,
        'estrelas_max' : estrelas_max,
        'diaria_min' : diaria_min,
        'diaria_max' : diaria_max,
        'limit': limit,
        'offset': off_set
    }

consulta_com_cidade = "SELECT * FROM hoteis \
                WHERE cidade = ? and (estrelas >= ? and estrelas <= ?)\
                and (valor_diaria >= ? and valor_diaria <= ?)\
                LIMIT? OFFSET?"

consulta_sem_cidade = "SELECT * FROM hoteis \
                WHERE (estrelas >= ? and estrelas <= ?)\
                and (valor_diaria >= ? and valor_diaria <= ?)\
                LIMIT? OFFSET?"

