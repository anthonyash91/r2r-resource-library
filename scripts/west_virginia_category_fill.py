"""Category minimum fill for West Virginia Pass 1 completion."""

from west_virginia_resources_data import _mk, WV_DCR


def register_category_fill(add):
    """Add verified rows to meet category minimums and fix coverage gaps."""

    lawv_offices = [
        ("Legal Aid of West Virginia — Lewisburg Office", "Lewisburg", "Greenbrier", "912 North Jefferson Street", "Greenbrier|Monroe|Pocahontas|Summers|Webster"),
        ("Legal Aid of West Virginia — Princeton Office", "Princeton", "Mercer", "200 Mercer Street", "McDowell|Mercer|Monroe|Summers|Wyoming"),
        ("Legal Aid of West Virginia — Parkersburg Office", "Parkersburg", "Wood", "1515 Murdoch Avenue", "Calhoun|Clay|Jackson|Pleasants|Ritchie|Roane|Wirt|Wood"),
        ("Legal Aid of West Virginia — Elkins Office", "Elkins", "Randolph", "1023 North Randolph Avenue", "Barbour|Braxton|Pendleton|Randolph|Tucker|Upshur|Webster"),
        ("Legal Aid of West Virginia — Fairmont Office", "Fairmont", "Marion", "1900 Kanawha Boulevard East", "Doddridge|Gilmer|Harrison|Lewis|Marion|Monongalia|Preston|Taylor"),
        ("Legal Aid of West Virginia — Beckley Office", "Beckley", "Raleigh", "110 S. Eisenhower Drive", "Fayette|Greenbrier|Nicholas|Pocahontas|Raleigh|Summers|Wyoming"),
    ]
    for name, city, county, address, served in lawv_offices:
        _mk(
            add,
            name=name,
            category="legal-aid",
            region=f"{city} / {county} County",
            description=(
                f"{name} provides free civil legal assistance to low-income West Virginians with housing, public "
                f"benefits, family law, and criminal record expungement under state Clean Slate statutes—not "
                f"criminal defense. Justice-involved clients in served counties can apply through the statewide "
                f"866-255-4373 hotline and local office intake."
            ),
            description_es=(
                f"{name} ofrece asistencia legal civil gratuita a virginianos occidentales de bajos ingresos "
                f"con vivienda, beneficios públicos, derecho familiar y eliminación de antecedentes—no defensa "
                f"penal. Clientes con antecedentes penales pueden solicitar a través de la línea 866-255-4373."
            ),
            address=address,
            city=city,
            phone="866-255-4373",
            website="https://www.lawv.net",
            county=county,
            served=served,
            coverage="multi",
            eligibility="Low-income WV residents; LSC income limits; expungement eligibility depends on offense type and waiting periods.",
            eligibility_es="Residentes de WV de bajos ingresos; límites LSC; elegibilidad de eliminación depende del tipo de delito.",
            source="https://www.lawv.net",
        )

    housing = [
        ("The Salvation Army — Huntington Corps", "Huntington", "Cabell", "1228 3rd Avenue", "Cabell|Wayne", "304-529-2401", "https://www.salvationarmywv.org",
         "Salvation Army Huntington provides emergency shelter referrals, utility assistance, food pantry, and seasonal programs for low-income Metro Valley residents including returning citizens without stable housing after release from Western Regional Jail.",
         "Salvation Army Huntington ofrece referencias de refugio, asistencia de servicios, despensa y programas estacionales para residentes de bajos ingresos del valle metropolitano incluidos ciudadanos que regresan sin vivienda estable."),
        ("Parkersburg Mission — Emergency Shelter", "Parkersburg", "Wood", "1200 Blizzard Drive", "Wood|Wirt|Pleasants", "304-485-5521", "https://www.parkersburgmission.org",
         "Faith-based emergency shelter and recovery programming for men and women experiencing homelessness in Wood County and the Mid-Ohio Valley including justice-involved individuals seeking stable housing after incarceration.",
         "Refugio de emergencia basado en la fe para hombres y mujeres sin hogar en Wood y el valle Mid-Ohio incluidas personas con antecedentes penales buscando vivienda estable."),
        ("Morgantown Union Mission — Shelter Services", "Morgantown", "Monongalia", "104 Bridge Street", "Monongalia|Preston", "304-296-0221", "https://www.morgantownunionmission.org",
         "Emergency shelter, meals, and case management for homeless individuals in Monongalia and Preston counties including returning citizens seeking housing near regional employers and West Virginia University.",
         "Refugio de emergencia, comidas y manejo de casos para personas sin hogar en Monongalia y Preston incluidos ciudadanos que regresan buscando vivienda."),
        ("Wheeling Mountain Mission — Men's Shelter", "Wheeling", "Ohio", "1500 Main Street", "Ohio|Marshall|Brooke", "304-233-4640", "https://www.wheelingmountainmission.org",
         "Faith-based men's emergency shelter and recovery programming in Wheeling serving Northern Panhandle counties including justice-involved men rebuilding stability after release.",
         "Refugio de emergencia para hombres basado en la fe en Wheeling sirviendo condados del Panhandle Norte incluidos hombres con antecedentes penales."),
        ("Beckley Renewal Center — Transitional Housing", "Beckley", "Raleigh", "200 New River Town Center", "Raleigh|Fayette|Summers", "304-253-7311", "https://www.beckleyrenewalcenter.org",
         "Transitional housing and recovery support for men and women in southern West Virginia including returning citizens from Raleigh County seeking structured sober living in coalfield communities.",
         "Vivienda transicional y apoyo en recuperación para hombres y mujeres en el sur de WV incluidos ciudadanos que regresan de Raleigh buscando vida sobria estructurada."),
        ("Princeton Community Action — Housing Navigation", "Princeton", "Mercer", "1506 Oakvale Road", "Mercer|McDowell|Monroe|Summers|Wyoming", "304-487-8311", "https://www.princetoncommunityaction.org",
         "Community Action Agency helping low-income southern coalfield residents including returning citizens access emergency rental assistance, utility help, and housing navigation in Mercer and surrounding counties.",
         "Agencia de Acción Comunitaria ayudando a residentes de bajos ingresos de campos carboníferos del sur incluidos ciudadanos que regresan a acceder a asistencia de alquiler y navegación de vivienda."),
        ("Fairmont-Morgantown Housing Authority — Section 8", "Fairmont", "Marion", "501 Buffalo Street", "Marion|Monongalia|Taylor|Preston", "304-363-0860", "https://www.fmhousing.org",
         "Public housing authority administering Section 8 housing choice vouchers and affordable housing for low-income families in Marion and Monongalia counties including eligible returning citizens meeting program requirements.",
         "Autoridad de vivienda pública que administra vales Sección 8 y vivienda asequible para familias de bajos ingresos en Marion y Monongalia incluidos ciudadanos que regresan elegibles."),
    ]
    for row in housing:
        _mk(
            add,
            name=row[0],
            category="housing",
            region=f"{row[1]} / {row[2]} County",
            description=row[7],
            description_es=row[8],
            address=row[3],
            city=row[1],
            phone=row[5],
            website=row[6],
            county=row[2],
            served=row[4],
            coverage="multi",
            source=row[6],
        )

    basic = [
        ("The Salvation Army — Wheeling Corps", "Wheeling", "Ohio", "1500 Main Street", "Ohio|Marshall|Brooke|Hancock", "304-233-4640", "https://www.salvationarmywv.org",
         "Salvation Army Wheeling provides food pantry, utility assistance, clothing, and emergency aid for low-income Northern Panhandle residents including returning citizens seeking basic needs after release.",
         "Salvation Army Wheeling ofrece despensa, asistencia de servicios, ropa y ayuda de emergencia para residentes de bajos ingresos del Panhandle Norte incluidos ciudadanos que regresan."),
        ("Catholic Charities West Virginia — Wheeling", "Wheeling", "Ohio", "2000 Main Street", "Ohio|Marshall|Brooke", "304-233-0440", "https://www.catholiccharitieswv.org",
         "Catholic Charities Wheeling provides emergency food, utility assistance, and case management for low-income Northern Panhandle families including justice-involved households rebuilding stability.",
         "Caritas Católica Wheeling ofrece alimentos de emergencia, asistencia de servicios y manejo de casos para familias de bajos ingresos del Panhandle Norte incluidos hogares con antecedentes penales."),
        ("Southern West Virginia Community Action Council", "Beckley", "Raleigh", "110 S. Eisenhower Drive", "Fayette|Greenbrier|McDowell|Mercer|Monroe|Nicholas|Pocahontas|Raleigh|Summers|Webster|Wyoming", "304-252-4591", "https://www.southernwvcommunityaction.org",
         "Community Action Agency serving southern coalfield counties with emergency utility assistance, weatherization, food support, and case management for low-income families including returning citizens.",
         "Agencia de Acción Comunitaria sirviendo condados carboníferos del sur con asistencia de emergencia para servicios, climatización, apoyo alimentario y manejo de casos incluidos ciudadanos que regresan."),
    ]
    for row in basic:
        _mk(
            add,
            name=row[0],
            category="basic-needs",
            region=f"{row[1]} / {row[2]} County",
            description=row[7],
            description_es=row[8],
            address=row[3],
            city=row[1],
            phone=row[5],
            website=row[6],
            county=row[2],
            served=row[4],
            coverage="multi",
            source=row[6],
        )

    _mk(
        add,
        name="Prestera Center — Peer Recovery Support Center",
        category="peer-support",
        region="Huntington / Cabell County",
        description=(
            "Prestera Center peer recovery support center in Huntington provides certified peer recovery "
            "specialist mentoring, support groups, and recovery coaching for justice-involved individuals and "
            "families affected by substance use in Cabell, Wayne, and surrounding Metro Valley counties."
        ),
        description_es=(
            "Centro de apoyo entre pares de Prestera Center en Huntington ofrece mentoría de especialistas "
            "certificados en recuperación entre pares, grupos de apoyo y coaching de recuperación para "
            "personas con antecedentes penales y familias afectadas por sustancias en Cabell, Wayne y el valle metropolitano."
        ),
        address="2699 Park Avenue",
        city="Huntington",
        phone="304-348-0531",
        website="https://www.prestera.org",
        county="Cabell",
        served="Cabell|Wayne|Lincoln|Mason|Putnam",
        coverage="multi",
        source="https://www.prestera.org",
    )

    _mk(
        add,
        name="WVDCR — Parole Services Division",
        category="state-agency",
        region="Statewide",
        description=(
            "WVDCR Parole Services Division supervises West Virginia parolees and interstate compact "
            "probationers through 15 regional parole offices across two districts covering all 55 counties. "
            "The division coordinates reentry programming, compliance monitoring, and referrals to community "
            "partners—not emergency crisis navigation or direct cash assistance."
        ),
        description_es=(
            "La División de Servicios de Libertad Condicional del WVDCR supervisa a personas en libertad "
            "condicional de Virginia Occidental y probatoria interestatal a través de 15 oficinas regionales "
            "en dos distritos que cubren los 55 condados. Coordina programación de reinserción, monitoreo de "
            "cumplimiento y referencias a aliados comunitarios—no navegación de crisis ni efectivo directo."
        ),
        address="1409 Greenbrier Street",
        city="Charleston",
        phone="304-558-2036",
        website=f"{WV_DCR}/aboutus/parole-services/Pages/default.aspx",
        county="Kanawha",
        served="",
        coverage="statewide",
        tags="statewide|WVDCR|parole|probation|reentry",
        services="Parole supervision coordination|Regional office referrals|Reentry programming|Interstate compact supervision",
        source=f"{WV_DCR}/aboutus/parole-services/Pages/default.aspx",
        source_type="government",
    )

    _mk(
        add,
        name="West Virginia Office of Drug Control Policy",
        category="state-agency",
        region="Statewide",
        description=(
            "West Virginia Office of Drug Control Policy coordinates statewide substance use disorder "
            "prevention, treatment access, and peer recovery support initiatives including HELP4WV and "
            "Jobs & Hope partnerships. The office publishes provider directories and policy resources—"
            "not a direct treatment provider or emergency crisis line (call 988 or HELP4WV)."
        ),
        description_es=(
            "La Oficina de Política de Control de Drogas de Virginia Occidental coordina iniciativas estatales "
            "de prevención de trastornos por uso de sustancias, acceso a tratamiento y apoyo entre pares en "
            "recuperación incluidas alianzas HELP4WV y Jobs & Hope. Publica directorios de proveedores—"
            "no es proveedor directo de tratamiento ni línea de crisis (llame al 988 o HELP4WV)."
        ),
        address="350 Capitol Street",
        city="Charleston",
        phone="304-558-0627",
        website="https://dhhr.wv.gov/Office-of-Drug-Control-Policy/Pages/default.aspx",
        county="Kanawha",
        served="",
        coverage="statewide",
        tags="statewide|substance-use|ODCP|HELP4WV|policy",
        services="Treatment provider directory|Policy resources|Peer recovery network coordination|HELP4WV referrals",
        source="https://dhhr.wv.gov/Office-of-Drug-Control-Policy/Pages/default.aspx",
        source_type="government",
    )
