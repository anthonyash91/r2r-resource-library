"""Illinois Pass 2 rural depth — verified direct-service rows for thin downstate counties."""


def register_rural_depth(add):
    """Add healthcare, legal-aid, and SUD depth for 13 Tier A-weak rural counties."""

    shawnee_south = (
        "Alexander|Edwards|Franklin|Gallatin|Hamilton|Hardin|Jackson|Johnson|Massac|"
        "Perry|Pope|Pulaski|Saline|Union|Wabash|Wayne|White|Williamson"
    )

    add(
        name="Shawnee Health Service — Southern Illinois FQHC",
        category="healthcare",
        region="Carterville / Southern Illinois",
        description=(
            "Shawnee Health Service is a Federally Qualified Health Center providing integrated primary "
            "care, behavioral health, dental, pharmacy, and addiction medicine on a sliding fee scale "
            "for uninsured and Medicaid patients in southern Illinois. Clinical sites operate in Jackson "
            "and Williamson counties while Shawnee Alliance social services reach 18 rural southern "
            "counties. Justice-involved returning citizens can establish medical homes, access MAT, "
            "and receive behavioral health counseling after release—not a walk-in crisis line."
        ),
        description_es=(
            "Shawnee Health Service es un Centro de Salud Calificado Federal (FQHC) que ofrece atención "
            "primaria integrada, salud conductual, dental, farmacia y medicina de adicciones con tarifa "
            "escalonada para pacientes sin seguro o con Medicaid en el sur de Illinois. Los sitios "
            "clínicos operan en los condados Jackson y Williamson mientras Shawnee Alliance llega a 18 "
            "condados rurales del sur. Ciudadanos que regresan pueden establecer un hogar médico y "
            "acceder a TMO y consejería conductual después de la liberación."
        ),
        address="109 California Street",
        city="Carterville",
        phone="618-985-1491",
        email="",
        website="https://www.shawneehealth.com",
        eligibility=(
            "Open to all southern Illinois residents regardless of insurance status; sliding fee scale "
            "available; justice-involved adults accepted for primary care and behavioral health."
        ),
        eligibility_es=(
            "Abierto a residentes del sur de Illinois sin importar seguro; tarifa escalonada disponible; "
            "adultos con antecedentes penales aceptados para atención primaria y salud conductual."
        ),
        notes=(
            "Call 618-985-1491 or visit shawneehealth.com for the nearest clinic; addiction medicine and "
            "counseling available at Carbondale, Marion, Murphysboro, and Carterville sites."
        ),
        notes_es=(
            "Llame al 618-985-1491 o visite shawneehealth.com para la clínica más cercana; medicina de "
            "adicciones y consejería disponibles en Carbondale, Marion, Murphysboro y Carterville."
        ),
        hours="Monday–Friday; call for clinic-specific hours",
        tags="illinois|FQHC|healthcare|behavioral-health|MAT|southern-illinois|reentry",
        services=(
            "Primary care|Behavioral health counseling|Dental care|Addiction medicine|"
            "Medication-assisted treatment|Sliding fee scale|Pharmacy services"
        ),
        county="Williamson",
        served_counties=shawnee_south,
        coverage="multi",
        _source="https://www.shawneehealth.com/about-us/",
        _source_type="nonprofit",
        _confidence="high",
    )

    add(
        name="Shawnee Health Service — Addiction Medicine & Recovery",
        category="substance-use-treatment",
        region="Southern Illinois",
        description=(
            "Shawnee Health Service provides outpatient substance use disorder treatment including "
            "medication-assisted recovery (buprenorphine, naltrexone), counseling, and integrated "
            "behavioral health for justice-involved adults in southern Illinois FQHC clinics. Staff "
            "coordinate with IDOC parole agents and rural recovery partners across 18 southern "
            "counties served by Shawnee Alliance—not residential detox; call for intake assessment."
        ),
        description_es=(
            "Shawnee Health Service ofrece tratamiento ambulatorio de trastornos por uso de sustancias "
            "incluyendo recuperación asistida con medicamentos (buprenorfina, naltrexona), consejería "
            "y salud conductual integrada para adultos con antecedentes penales en clínicas FQHC del "
            "sur de Illinois. El personal coordina con agentes de libertad condicional del IDOC y "
            "aliados de recuperación rurales en 18 condados del sur."
        ),
        address="400 South Lewis Lane",
        city="Carbondale",
        phone="618-985-1491",
        email="",
        website="https://www.shawneehealth.com",
        eligibility=(
            "Adults with substance use disorders in southern Illinois; Medicaid and sliding fee accepted; "
            "justice-involved clients welcome per program policy."
        ),
        eligibility_es=(
            "Adultos con trastornos por uso de sustancias en el sur de Illinois; Medicaid y tarifa "
            "escalonada aceptados; clientes con antecedentes penales bienvenidos según política."
        ),
        notes="Call 618-985-1491 for SUD intake; Carbondale and Marion sites offer MAT and counseling.",
        notes_es="Llame al 618-985-1491 para admisión de TUS; sitios de Carbondale y Marion ofrecen TMO y consejería.",
        hours="Contact for current clinic hours",
        tags="illinois|SUD|MAT|recovery|southern-illinois|reentry",
        services="Outpatient substance use treatment|Medication-assisted treatment|Counseling|Recovery supports",
        county="Jackson",
        served_counties=shawnee_south,
        coverage="multi",
        _source="https://www.shawneehealth.com",
        _source_type="nonprofit",
        _confidence="high",
    )

    _county_health_clinic(
        add,
        name="Cass County Health Clinic — FQHC",
        category="healthcare",
        county="Cass",
        city="Virginia",
        address="331 South Main Street",
        phone="217-452-3057",
        website="https://www.casscohealth.org",
        description=(
            "Cass County Health Clinic is a Federally Qualified Health Center operated by the Cass County "
            "Health Department with primary care, behavioral health counseling, dental, and WIC services "
            "in Virginia and Beardstown on a sliding fee scale. Returning citizens in rural western Illinois "
            "can establish a medical home, access grief and domestic-violence counseling, and receive "
            "Medicaid enrollment help after release from Logan Correctional Center or local jails."
        ),
        description_es=(
            "Cass County Health Clinic es un FQHC operado por el Departamento de Salud del condado Cass "
            "con atención primaria, consejería conductual, dental y WIC en Virginia y Beardstown con "
            "tarifa escalonada. Ciudadanos que regresan en el oeste rural de Illinois pueden establecer "
            "un hogar médico y recibir ayuda de inscripción en Medicaid."
        ),
        source="https://www.casscohealth.org/healthclinic",
    )

    _county_health_clinic(
        add,
        name="Mason County Health Department",
        category="healthcare",
        county="Mason",
        city="Havana",
        address="1002 East Laurel Avenue",
        phone="309-543-2201",
        website="https://www.mchdept.com",
        description=(
            "Mason County Health Department provides public health, immunizations, WIC, maternal-child "
            "health, and environmental health services for Havana and rural Mason County residents "
            "including justice-involved individuals rebuilding stability after release from local jails "
            "or IDOC custody. Staff connect clients to regional FQHC partners and Illinois workNet "
            "employment services in western Illinois."
        ),
        description_es=(
            "El Departamento de Salud del condado Mason ofrece salud pública, inmunizaciones, WIC, salud "
            "materno-infantil y servicios ambientales para residentes de Havana y el condado Mason rural, "
            "incluidas personas con antecedentes penales que reconstruyen estabilidad."
        ),
        source="https://www.mchdept.com",
    )

    _county_health_clinic(
        add,
        name="McDonough County Health Department",
        category="healthcare",
        county="McDonough",
        city="Macomb",
        address="505 East Jackson Street",
        phone="309-837-9951",
        website="https://www.mchdept.com",
        description=(
            "McDonough County Health Department delivers immunizations, WIC, breast and cervical cancer "
            "screenings, family case management, and communicable disease follow-up for Macomb and rural "
            "McDonough County including Western Illinois University communities and returning citizens "
            "after release. Coordinates with Western Illinois Regional Council and Prairie State Legal "
            "Services for wraparound reentry support in west-central Illinois."
        ),
        description_es=(
            "El Departamento de Salud del condado McDonough ofrece inmunizaciones, WIC, detección de "
            "cáncer de mama y cuello uterino, manejo de casos familiares y seguimiento de enfermedades "
            "transmisibles para Macomb y el condado McDonough rural, incluidos ciudadanos que regresan."
        ),
        source="https://www.mchdept.com",
    )

    _county_health_clinic(
        add,
        name="Douglas County Health Department",
        category="healthcare",
        county="Douglas",
        city="Tuscola",
        address="1250 East US Highway 36",
        phone="217-253-4137",
        website="https://www.dchealthil.org",
        description=(
            "Douglas County Health Department operates a community health center, dental clinic, WIC, "
            "family case management, and environmental health programs in Tuscola for east-central "
            "Illinois rural residents including justice-involved individuals between Champaign and "
            "Decatur. Provides immunizations, reproductive health, and health education with referral "
            "linkages to Prairie Center and Land of Lincoln Legal Aid regional offices."
        ),
        description_es=(
            "El Departamento de Salud del condado Douglas opera un centro de salud comunitario, clínica "
            "dental, WIC, manejo de casos familiares y programas de salud ambiental en Tuscola para "
            "residentes rurales del centro-este de Illinois, incluidas personas con antecedentes penales."
        ),
        source="https://www.dchealthil.org",
    )

    _county_health_clinic(
        add,
        name="Montgomery County Health Department",
        category="healthcare",
        county="Montgomery",
        city="Hillsboro",
        address="11191 Illinois Route 185",
        phone="217-532-2001",
        website="https://montgomerycountyil.gov/health-department/",
        description=(
            "Montgomery County Health Department provides WIC, immunizations, maternal-child health, "
            "environmental health inspections, and disease prevention services in Hillsboro and Litchfield "
            "for rural residents including returning citizens on probation or parole. Connects clients to "
            "Montgomery County Workforce Board, Land of Lincoln Legal Aid western region, and regional "
            "hospitals for specialty care in south-central Illinois."
        ),
        description_es=(
            "El Departamento de Salud del condado Montgomery ofrece WIC, inmunizaciones, salud "
            "materno-infantil, inspecciones de salud ambiental y prevención de enfermedades en Hillsboro "
            "y Litchfield para residentes rurales, incluidos ciudadanos que regresan bajo supervisión."
        ),
        source="https://montgomerycountyil.gov/health-department/",
    )

    _county_health_clinic(
        add,
        name="Henderson County Health Department",
        category="healthcare",
        county="Henderson",
        city="Gladstone",
        address="208 West Elm Street",
        phone="309-627-2812",
        website="https://hendcohealth.com",
        description=(
            "Henderson County Health Department provides WIC, home health, senior services, environmental "
            "health, and a community food pantry for Gladstone and rural Henderson County along the "
            "Mississippi River including justice-involved residents returning from regional jails. Staff "
            "coordinate with River Bend Foodbank partners, Prairie State Legal Services Galesburg office, "
            "and Knox County providers for specialty referrals."
        ),
        description_es=(
            "El Departamento de Salud del condado Henderson ofrece WIC, salud en el hogar, servicios "
            "para personas mayores, salud ambiental y despensa comunitaria para Gladstone y el condado "
            "Henderson rural junto al río Mississippi, incluidos residentes con antecedentes penales."
        ),
        source="https://hendcohealth.com/about-us/",
    )

    add(
        name="Wabash Community Health Center — FQHC",
        category="healthcare",
        region="Mount Carmel / Wabash County",
        description=(
            "Wabash Community Health Center is a Federally Qualified Health Center partnership between "
            "Wabash County Health Department and Wabash General Hospital offering primary care, "
            "behavioral health, psychiatric services, and reproductive health on a sliding fee scale "
            "in Mount Carmel. Justice-involved adults in southeastern Illinois can access integrated "
            "medical and mental health care after release—not emergency hospital services."
        ),
        description_es=(
            "Wabash Community Health Center es un FQHC en asociación entre el Departamento de Salud del "
            "condado Wabash y Wabash General Hospital que ofrece atención primaria, salud conductual, "
            "servicios psiquiátricos y salud reproductiva con tarifa escalonada en Mount Carmel. Adultos "
            "con antecedentes penales pueden acceder a atención médica y de salud mental integrada."
        ),
        address="1123 North Chestnut Street",
        city="Mount Carmel",
        phone="618-263-3873",
        email="",
        website="https://www.wabashhealth.org",
        eligibility="Open to Wabash County residents; sliding fee scale; justice-involved adults accepted.",
        eligibility_es="Abierto a residentes del condado Wabash; tarifa escalonada; adultos con antecedentes penales aceptados.",
        notes="Call 618-263-3873; health department at 130 W 7th St coordinates FQHC appointments.",
        notes_es="Llame al 618-263-3873; el departamento de salud en 130 W 7th St coordina citas del FQHC.",
        hours="Monday–Thursday 7 a.m.–5 p.m.; Friday 8 a.m.–noon",
        tags="illinois|FQHC|healthcare|behavioral-health|wabash|reentry",
        services="Primary care|Behavioral health|Psychiatric services|Reproductive health|Sliding fee scale",
        county="Wabash",
        served_counties="Wabash",
        coverage="single",
        _source="https://www.wabashhealth.org",
        _source_type="government",
        _confidence="high",
    )

    add(
        name="Prairie State Legal Services — Galesburg Office",
        category="legal-aid",
        region="Galesburg / Western Illinois",
        description=(
            "Prairie State Legal Services Galesburg office provides free civil legal aid to low-income "
            "residents of Henderson, Knox, McDonough, and Warren counties including expungement, "
            "housing and eviction defense, public benefits appeals, and family law for justice-involved "
            "clients in rural western Illinois. Apply online at pslegal.org or call for intake—does not "
            "handle criminal defense."
        ),
        description_es=(
            "La oficina de Galesburg de Prairie State Legal Services ofrece asistencia legal civil gratuita "
            "a residentes de bajos ingresos de los condados Henderson, Knox, McDonough y Warren, incluida "
            "eliminación de antecedentes, defensa de vivienda y desalojo, apelaciones de beneficios públicos "
            "y derecho familiar para clientes con antecedentes penales."
        ),
        address="311 East Main Street, Suite 302",
        city="Galesburg",
        phone="309-343-2141",
        email="",
        website="https://www.pslegal.org",
        eligibility="Low-income residents of Henderson, Knox, McDonough, or Warren counties; income limits apply.",
        eligibility_es="Residentes de bajos ingresos de Henderson, Knox, McDonough o Warren; aplican límites de ingresos.",
        notes="Toll-free 800-331-0617; apply online at pslegal.org/get-legal-help.",
        notes_es="Línea gratuita 800-331-0617; solicite en línea en pslegal.org/get-legal-help.",
        hours="Monday–Friday business hours",
        tags="illinois|legal-aid|western-illinois|reentry|expungement",
        services="Civil legal aid|Expungement assistance|Housing defense|Benefits appeals|Family law",
        county="Knox",
        served_counties="Henderson|Knox|McDonough|Warren",
        coverage="multi",
        _source="https://www.pslegal.org/our-offices",
        _source_type="nonprofit",
        _confidence="high",
    )

    add(
        name="Southern Illinois Community Action — Emergency Assistance",
        category="basic-needs",
        region="Marion / Southern Illinois",
        description=(
            "Southern Illinois Community Action Agency provides emergency financial assistance, LIHEAP "
            "energy aid, weatherization, and case management for low-income residents in 12 southern "
            "Illinois counties including Edwards, Gallatin, Hamilton, Hardin, Pope, Saline, and Wabash. "
            "Returning citizens can access utility and rent assistance, weatherization, and referrals to "
            "Shawnee Health and Land of Lincoln Legal Aid after release."
        ),
        description_es=(
            "Southern Illinois Community Action Agency ofrece asistencia financiera de emergencia, ayuda "
            "energética LIHEAP, climatización y manejo de casos para residentes de bajos ingresos en 12 "
            "condados del sur de Illinois incluidos Edwards, Gallatin, Hamilton, Hardin, Pope, Saline "
            "y Wabash. Ciudadanos que regresan pueden acceder a ayuda de servicios públicos y referencias."
        ),
        address="1100 North Carbon Street",
        city="Marion",
        phone="618-997-5567",
        email="",
        website="https://www.sicacaa.org",
        eligibility="Low-income residents of served southern Illinois counties; documentation required.",
        eligibility_es="Residentes de bajos ingresos de condados servidos del sur de Illinois; se requiere documentación.",
        notes="Call 618-997-5567 or visit sicacaa.org for current program availability and intake.",
        notes_es="Llame al 618-997-5567 o visite sicacaa.org para disponibilidad e admisión actual.",
        hours="Monday–Friday business hours",
        tags="illinois|community-action|basic-needs|southern-illinois|reentry",
        services="Emergency assistance|Utility assistance|Weatherization|Case management|Referrals",
        county="Williamson",
        served_counties=(
            "Edwards|Franklin|Gallatin|Hamilton|Hardin|Jefferson|Johnson|Marion|Perry|Pope|"
            "Saline|Union|Wabash|Wayne|White|Williamson"
        ),
        coverage="multi",
        _source="https://www.sicacaa.org",
        _source_type="nonprofit",
        _confidence="high",
    )


def _county_health_clinic(add, *, name, category, county, city, address, phone, website, description, description_es, source):
    add(
        name=name,
        category=category,
        region=f"{city} / {county} County",
        description=description,
        description_es=description_es,
        address=address,
        city=city,
        phone=phone,
        email="",
        website=website,
        eligibility=(
            f"Open to {county} County, Illinois residents; justice-involved individuals generally welcome; "
            "insurance and sliding fee options vary by service."
        ),
        eligibility_es=(
            f"Abierto a residentes del condado {county}, Illinois; personas con antecedentes penales "
            "generalmente bienvenidas; opciones de seguro y tarifa escalonada varían."
        ),
        notes=f"Call {phone} or visit {website} to confirm walk-in hours and required documents.",
        notes_es=f"Llame al {phone} o visite {website} para confirmar horarios y documentos requeridos.",
        hours="Contact for current hours",
        tags=f"illinois|healthcare|{county.lower()}|reentry|rural",
        services="Primary care|Immunizations|WIC|Health education|Referrals",
        county=county,
        served_counties=county,
        coverage="single",
        _source=source,
        _source_type="government",
        _confidence="high",
    )
