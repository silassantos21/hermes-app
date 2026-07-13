from models import Local, Medico

DADOS = [
    {
        "nome": "Dr. Carlos Mendes", "crm": "CRM-SP 123.456", "especialidade": "Cardiologia",
        "status": "disponivel", "ultimo_reporte": "12 min atrás", "reportado_por": "Rafael S.", "total_reportes": 47,
        "locais": [
            {"endereco": "Av. Paulista, 1500 · Bela Vista, SP",     "dias": "Seg, Qua, Sex", "horario": "08h–12h / 14h–18h", "verificado": True,  "dias_verif": 8},
            {"endereco": "R. Teodoro Sampaio, 352 · Pinheiros, SP", "dias": "Ter, Qui",      "horario": "13h–18h",            "verificado": False, "dias_verif": 75},
        ],
    },
    {
        "nome": "Dra. Ana Paula Santos", "crm": "CRM-SP 234.567", "especialidade": "Dermatologia",
        "status": "atrasado", "ultimo_reporte": "5 min atrás", "reportado_por": "Marcos L.", "total_reportes": 32,
        "locais": [
            {"endereco": "R. Oscar Freire, 800 · Jardins, SP",           "dias": "Ter, Qui", "horario": "09h–13h / 15h–19h", "verificado": True, "dias_verif": 12},
            {"endereco": "Av. Brig. Luís Antônio, 500 · Bela Vista, SP", "dias": "Seg, Sex", "horario": "08h–12h",            "verificado": True, "dias_verif": 45},
        ],
    },
    {
        "nome": "Dr. Roberto Ferreira", "crm": "CRM-RJ 345.678", "especialidade": "Ortopedia",
        "status": "indisponivel", "ultimo_reporte": "1h atrás", "reportado_por": "Carla M.", "total_reportes": 28,
        "locais": [
            {"endereco": "R. das Laranjeiras, 340 · Laranjeiras, RJ", "dias": "Seg, Qua, Sex", "horario": "07h–11h", "verificado": True, "dias_verif": 30},
        ],
    },
    {
        "nome": "Dra. Mariana Costa", "crm": "CRM-SP 456.789", "especialidade": "Pediatria",
        "status": "disponivel", "ultimo_reporte": "3 min atrás", "reportado_por": "Lucas P.", "total_reportes": 61,
        "locais": [
            {"endereco": "Av. Rebouças, 1200 · Pinheiros, SP", "dias": "Seg–Qua", "horario": "08h–17h", "verificado": True, "dias_verif": 3},
            {"endereco": "R. Vergueiro, 1000 · Liberdade, SP", "dias": "Qui, Sex", "horario": "09h–16h", "verificado": True, "dias_verif": 22},
        ],
    },
    {
        "nome": "Dr. Paulo Alves", "crm": "CRM-MG 567.890", "especialidade": "Neurologia",
        "status": "atrasado", "ultimo_reporte": "8 min atrás", "reportado_por": "Fernanda R.", "total_reportes": 19,
        "locais": [
            {"endereco": "Av. Afonso Pena, 2500 · Centro, BH",        "dias": "Seg, Qua",      "horario": "08h–12h", "verificado": True,  "dias_verif": 18},
            {"endereco": "R. Cláudio Manoel, 100 · Funcionários, BH", "dias": "Ter, Qui, Sáb", "horario": "13h–17h", "verificado": False, "dias_verif": 82},
        ],
    },
    {
        "nome": "Dra. Fernanda Lima", "crm": "CRM-SP 678.901", "especialidade": "Endocrinologia",
        "status": "disponivel", "ultimo_reporte": "22 min atrás", "reportado_por": "Bruno T.", "total_reportes": 38,
        "locais": [
            {"endereco": "R. Vergueiro, 3185 · Vila Mariana, SP", "dias": "Seg, Qua, Sex", "horario": "10h–14h / 16h–19h", "verificado": True, "dias_verif": 15},
            {"endereco": "Av. Paulista, 900 · Bela Vista, SP",    "dias": "Ter, Qui",      "horario": "08h–12h",            "verificado": True, "dias_verif": 55},
        ],
    },
]


def seed_database(db):
    for data in DADOS:
        locais_data = data.pop("locais")
        medico = Medico(**data)
        db.add(medico)
        db.flush()
        for ld in locais_data:
            db.add(Local(medico_id=medico.id, **ld))
    db.commit()
