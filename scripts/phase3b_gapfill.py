"""Phase 3b small-county depth gap-fill.

Add a register_phase3b_{state_slug}(add) function per state, then import it from
scripts/build-{state-slug}-resources.py. See docs/prompts/multi-state-resource-research.md.
"""

DATE = "2026-06-23"


def _dfr_in(county, city, address, phone, website, region, desc_en, desc_es, services, tags):
    return dict(
        name=f"{county} County Division of Family Resources",
        category="financial-assistance",
        region=region,
        description=desc_en,
        description_es=desc_es,
        address=address,
        city=city,
        phone=phone,
        email="",
        website=website,
        eligibility=f"{county} County residents meeting income and program requirements for Medicaid, SNAP, TANF, or HIP; criminal record generally not a barrier.",
        eligibility_es=f"Residentes del condado {county} que cumplan requisitos de ingresos para Medicaid, SNAP, TANF o HIP; los antecedentes penales generalmente no son barrera.",
        notes="Apply online at fssabenefits.in.gov or visit the county DFR office; bring ID, Social Security card, and release documents if applicable.",
        notes_es="Solicite en fssabenefits.in.gov o visite la oficina DFR del condado; traiga identificación, tarjeta de Seguro Social y documentos de liberación si aplica.",
        hours="Monday–Friday, 8:00 a.m.–4:30 p.m.",
        tags=tags,
        services=services,
        county=county,
        served_counties=county,
        coverage="single",
        _source=website,
        _source_type="government",
        _confidence="high",
    )


def _jfs_desc_en(county: str, city: str) -> str:
    return (
        f"{county} County Job and Family Services is the county public benefits intake office in "
        f"{city}, administering Medicaid, SNAP, Ohio Works First cash assistance, and child care "
        f"subsidies for Ohio residents including justice-involved individuals establishing food and "
        f"health coverage after release. Staff assist with benefits.ohio.gov applications and "
        f"OhioMeansJobs workforce connections for fair-chance employment."
    )


def _jfs_desc_es(county: str, city: str) -> str:
    return (
        f"{county} County Job and Family Services es la oficina de admisión de beneficios públicos "
        f"del condado en {city}, que administra Medicaid, SNAP, asistencia en efectivo Ohio Works "
        f"First y subsidios de cuidado infantil para residentes de Ohio, incluidas personas con "
        f"antecedentes penales que establecen cobertura alimentaria y de salud después de la "
        f"liberación. El personal ayuda con solicitudes en benefits.ohio.gov y conexiones "
        f"OhioMeansJobs para empleo justo."
    )


def _dhs_desc_en(county: str, city: str) -> str:
    return (
        f"{county} County Department of Human Services Family Assistance office in {city} processes "
        f"SNAP, Families First, Medicaid, and TennCare applications for Tennessee residents including "
        f"returning citizens reestablishing food and health benefits after release from {county} "
        f"County Jail or state custody."
    )


def _dhs_desc_es(county: str, city: str) -> str:
    return (
        f"La oficina de Asistencia Familiar del Departamento de Servicios Humanos del condado {county} "
        f"en {city} procesa solicitudes de SNAP, Families First, Medicaid y TennCare para residentes "
        f"de Tennessee, incluidos ciudadanos que regresan que restablecen beneficios alimentarios y de "
        f"salud después de la liberación."
    )


def _dcbs_desc_en(county: str, city: str) -> str:
    return (
        f"DCBS Family Support office in {city} helps {county} County residents apply for Medicaid, SNAP, "
        f"KTAP, and child care assistance through kynect. Returning citizens and families rebuilding after "
        f"incarceration can establish health coverage and food benefits at this county office or online with "
        f"local staff assisting document verification."
    )


def _dcbs_desc_es(county: str, city: str) -> str:
    return (
        f"La oficina de Apoyo Familiar DCBS en {city} ayuda a residentes del condado {county} a solicitar "
        f"Medicaid, SNAP, KTAP y cuidado infantil a través de kynect, incluidos ciudadanos que regresan "
        f"de la encarcelación que restablecen beneficios alimentarios y de salud."
    )


def _jfs_oh(county, city, address, phone, website, region, desc_en, desc_es, hours="Monday–Friday, 7:30 a.m.–4:30 p.m."):
    return dict(
        name=f"{county} County Job and Family Services",
        category="financial-assistance",
        region=region,
        description=desc_en,
        description_es=desc_es,
        address=address,
        city=city,
        phone=phone,
        email="",
        website=website,
        eligibility=f"{county} County residents meeting income and program requirements for public benefits; criminal record generally not a barrier.",
        eligibility_es=f"Residentes del condado {county} que cumplan requisitos de ingresos para beneficios públicos; los antecedentes penales generalmente no son barrera.",
        notes="Apply online at benefits.ohio.gov or visit the county JFS office; bring ID, Social Security card, and release documents if applicable.",
        notes_es="Solicite en benefits.ohio.gov o visite la oficina JFS del condado; traiga identificación, tarjeta de Seguro Social y documentos de liberación si aplica.",
        hours=hours,
        tags=f"{county.lower()}|ohio|benefits|SNAP|Medicaid|reentry",
        services="Medicaid enrollment|SNAP application|Cash assistance|OhioMeansJobs connections|Restored citizen intake",
        county=county,
        served_counties=county,
        coverage="single",
        _source=website or "https://jfs.ohio.gov/about/local-agencies-directory/local-agencies-directory",
        _source_type="government",
        _confidence="high",
    )


def _dhs_tn(county, city, address, phone, region, desc_en, desc_es):
    return dict(
        name=f"{county} County Department of Human Services — Family Assistance",
        category="financial-assistance",
        region=region,
        description=desc_en,
        description_es=desc_es,
        address=address,
        city=city,
        phone=phone,
        email="",
        website="https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        eligibility=f"{county} County residents meeting income and household-size requirements for SNAP, Families First, Medicaid, and TennCare; criminal record generally not a barrier.",
        eligibility_es=f"Residentes del condado {county} que cumplan requisitos de ingresos para SNAP, Families First, Medicaid y TennCare; los antecedentes penales generalmente no son barrera.",
        notes="Apply online at onedhs.tn.gov or call 1-866-311-4287; bring ID and release documents when establishing benefits after incarceration.",
        notes_es="Solicite en onedhs.tn.gov o llame al 1-866-311-4287; traiga identificación y documentos de liberación al establecer beneficios después de la encarcelación.",
        hours="Monday–Friday, 8:00 a.m.–4:30 p.m.",
        tags=f"{county.lower()}|tennessee|benefits|SNAP|Medicaid|reentry",
        services="SNAP enrollment|Medicaid and TennCare|Families First cash assistance|Child care certificates|Document upload assistance",
        county=county,
        served_counties=county,
        coverage="single",
        _source="https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        _source_type="government",
        _confidence="high",
    )


def register_phase3b_indiana(add, entries=None):
    """County DFR via registry + thin-county depth rows."""

    from county_benefits_registry import collect_financial_assistance_counties, register_county_benefits_indiana

    existing_fa = collect_financial_assistance_counties(entries or [])
    register_county_benefits_indiana(add, existing_fa)

    add(
        name="WorkOne — Greensburg",
        category="employment",
        region="Greensburg / Decatur County",
        description=(
            "WorkOne Greensburg is the Decatur County American Job Center connecting Southeast Indiana job seekers "
            "including justice-involved Hoosiers to career coaching, resume development, interview preparation, and "
            "employer referrals. Staff assist with unemployment navigation, skills training referrals, and federal "
            "bonding information for fair-chance hiring. The center serves Decatur and nine surrounding counties "
            "through the Region 9 workforce board."
        ),
        description_es=(
            "WorkOne Greensburg es el Centro de Empleo Americano del condado Decatur que conecta a buscadores de "
            "empleo del sureste de Indiana, incluidos hoosiers con antecedentes penales, con coaching de carrera, "
            "desarrollo de currículum, preparación para entrevistas y referencias a empleadores. El personal ayuda "
            "con navegación de desempleo, referencias de capacitación y información de fianza federal para contratación "
            "justa."
        ),
        address="422 East Central Avenue",
        city="Greensburg",
        phone="(812) 663-8597",
        email="",
        website="https://www.in.gov/dwd/workonesoutheast/locations/greensburg/",
        eligibility="Indiana residents seeking employment services; justice-involved individuals welcome at WorkOne centers statewide.",
        eligibility_es="Residentes de Indiana que buscan servicios de empleo; personas con antecedentes penales son bienvenidas en centros WorkOne.",
        notes="Call ahead to confirm current hours; unemployment claims must be filed online at Unemployment.IN.gov.",
        notes_es="Llame con anticipación para confirmar horarios; las solicitudes de desempleo deben presentarse en línea en Unemployment.IN.gov.",
        hours="Monday–Friday, 8:00 a.m.–4:30 p.m.; verify current schedule before visiting",
        tags="decatur|indiana|employment|WorkOne|reentry",
        services="Career coaching|Resume development|Job search assistance|Training referrals|Federal bonding information",
        county="Decatur",
        served_counties="Decatur",
        coverage="single",
        _source="https://www.in.gov/dwd/workonesoutheast/locations/greensburg/",
        _source_type="government",
        _confidence="high",
    )

    add(
        name="Howard County Community Supervision",
        category="probation-parole",
        region="Kokomo / Howard County",
        description=(
            "Howard County Community Supervision is the unified probation and community corrections department in "
            "Kokomo providing home detention, work release, reentry court programming, and evidence-based supervision "
            "for justice-involved individuals referred by local courts or the Indiana Department of Correction. The "
            "work release facility at 623 South Berkley houses up to 120 residents transitioning to employment while "
            "under intensive supervision. Reentry Court assists eligible offenders returning from incarceration over "
            "12–36 months of structured community supervision."
        ),
        description_es=(
            "Howard County Community Supervision es el departamento unificado de libertad condicional y correcciones "
            "comunitarias en Kokomo que ofrece detención domiciliaria, libertad bajo trabajo, tribunal de reinserción "
            "y supervisión basada en evidencia para personas referidas por tribunales locales o el IDOC. La instalación "
            "de libertad bajo trabajo aloja hasta 120 residentes en transición al empleo bajo supervisión intensiva."
        ),
        address="220 North Main Street",
        city="Kokomo",
        phone="(765) 456-2947",
        email="",
        website="https://www.in.gov/counties/howard/departments/community-supervision/",
        eligibility="Howard County justice-involved individuals referred by courts, prosecutors, or IDOC; program-specific offense criteria apply.",
        eligibility_es="Personas con antecedentes penales del condado Howard referidas por tribunales, fiscales o el IDOC; aplican criterios específicos del programa.",
        notes="Work release intake at 623 South Berkley; Reentry Court case manager (765) 456-2224; referral required for most programs.",
        notes_es="Admisión de libertad bajo trabajo en 623 South Berkley; administrador del Tribunal de Reinserción (765) 456-2224; se requiere referencia para la mayoría de programas.",
        hours="Monday–Friday business hours",
        tags="howard|indiana|probation|community-corrections|work-release|reentry",
        services="Work release|Home detention|Reentry Court|Probation supervision|Evidence-based case management",
        county="Howard",
        served_counties="Howard",
        coverage="single",
        _source="https://www.in.gov/counties/howard/departments/community-supervision/",
        _source_type="government",
        _confidence="high",
    )
    add(
        name="Kokomo Rescue Mission — Emergency Shelter",
        category="basic-needs",
        region="Kokomo / Howard County",
        description=(
            "Kokomo Rescue Mission provides emergency shelter, meals, clothing, and stabilization support for men, "
            "women, and families experiencing homelessness in Howard County including returning citizens without stable "
            "housing after release. The mission offers case management, recovery support referrals, and family assistance "
            "programs connecting guests to employment, benefits, and longer-term housing partners in north-central Indiana."
        ),
        description_es=(
            "Kokomo Rescue Mission ofrece refugio de emergencia, comidas, ropa y apoyo de estabilización para hombres, "
            "mujeres y familias sin hogar en el condado Howard, incluidos ciudadanos que regresan sin vivienda estable "
            "después de la liberación. La misión ofrece manejo de casos, referencias de apoyo de recuperación y "
            "programas de asistencia familiar que conectan a huéspedes con empleo, beneficios y aliados de vivienda."
        ),
        address="321 West Mulberry Street",
        city="Kokomo",
        phone="(765) 456-3838",
        email="missioninfo@rescuekokomo.org",
        website="https://www.kokomorescuemission.org",
        eligibility="Open to homeless individuals and families in Kokomo and Howard County; contact for intake requirements and shelter availability.",
        eligibility_es="Abierto a personas y familias sin hogar en Kokomo y el condado Howard; contacte para requisitos de admisión y disponibilidad.",
        notes="Call (765) 456-3838 for shelter availability and intake hours; probation or parole status may affect eligibility—confirm with staff.",
        notes_es="Llame al (765) 456-3838 para disponibilidad de refugio y horarios de admisión; el estado de libertad condicional puede afectar elegibilidad.",
        hours="Contact for current intake hours",
        tags="howard|indiana|shelter|basic-needs|reentry",
        services="Emergency shelter|Meals|Clothing|Case management|Recovery referrals|Family assistance",
        county="Howard",
        served_counties="Howard",
        coverage="single",
        _source="https://www.kokomorescuemission.org",
        _source_type="nonprofit",
        _confidence="high",
    )

    add(
        name="Hinds Career Center — Adult Education",
        category="education",
        region="Elwood / Tipton County",
        description=(
            "Hinds Career Center adult education program provides free High School Equivalency (HSE) preparation, "
            "English language instruction, and workforce credential pathways for adults in Tipton, Hamilton, and Madison "
            "counties including justice-involved learners rebuilding education credentials after incarceration. Instructors "
            "help students schedule orientation, connect to WorkOne employment services, and prepare for Indiana HSE testing."
        ),
        description_es=(
            "El programa de educación para adultos del Hinds Career Center ofrece preparación gratuita para la "
            "equivalencia de secundaria (HSE), instrucción en inglés y caminos hacia credenciales laborales para "
            "adultos en los condados Tipton, Hamilton y Madison, incluidos aprendices con antecedentes penales que "
            "reconstruyen credenciales educativas después de la encarcelación."
        ),
        address="1105 North 19th Street",
        city="Elwood",
        phone="(765) 552-4122",
        email="",
        website="https://www.in.gov/dwd/career-training-adult-ed/adult-ed/locations/",
        eligibility="Adults 18 and older in Tipton County seeking HSE or workforce credentials; no criminal-record restrictions stated.",
        eligibility_es="Adultos de 18 años o más en el condado Tipton que buscan HSE o credenciales laborales; sin restricciones de antecedentes indicadas.",
        notes="Register through Indiana Adult Education portal or call for orientation appointment; classes also serve Hamilton and Madison counties.",
        notes_es="Regístrese a través del portal de Educación para Adultos de Indiana o llame para cita de orientación; las clases también sirven a Hamilton y Madison.",
        hours="Contact for class schedules",
        tags="tipton|indiana|education|HSE|adult-ed|reentry",
        services="HSE preparation|English language instruction|Workforce credentials|Career coaching referrals|Orientation scheduling",
        county="Tipton",
        served_counties="Tipton|Hamilton|Madison",
        coverage="multi",
        _source="https://www.in.gov/dwd/career-training-adult-ed/adult-ed/locations/",
        _source_type="government",
        _confidence="high",
    )

    add(
        name="Bowen Health — Wabash",
        category="healthcare",
        region="Wabash / Wabash County",
        description=(
            "Bowen Health Wabash is a community behavioral health and primary care center providing outpatient mental "
            "health therapy, psychiatric services, addiction recovery treatment, and crisis stabilization for Wabash "
            "County residents including justice-involved individuals establishing care after release. The center has "
            "served Wabash residents since 1960 and offers walk-in crisis support through the 24-hour line at "
            "800-342-5653. Sliding-fee and Medicaid services available."
        ),
        description_es=(
            "Bowen Health Wabash es un centro comunitario de salud conductual y atención primaria que ofrece terapia "
            "ambulatoria de salud mental, servicios psiquiátricos, tratamiento de recuperación de adicciones y "
            "estabilización de crisis para residentes del condado Wabash, incluidas personas con antecedentes penales "
            "que establecen atención después de la liberación. Servicios con tarifa móvil y Medicaid disponibles."
        ),
        address="255 North Miami Street",
        city="Wabash",
        phone="(574) 385-3145",
        email="",
        website="https://www.bowenhealth.org/wabash-county",
        eligibility="Wabash County residents; justice-involved individuals accepted per program policy; Medicaid and sliding-fee available.",
        eligibility_es="Residentes del condado Wabash; personas con antecedentes penales aceptadas según política del programa; Medicaid y tarifa móvil disponibles.",
        notes="Crisis line 800-342-5653 or 988; facility relocating to 1649 Bowen Drive in September 2026—verify address before visiting.",
        notes_es="Línea de crisis 800-342-5653 o 988; la instalación se trasladará a 1649 Bowen Drive en septiembre de 2026—verifique la dirección.",
        hours="Monday–Thursday 8:00 a.m.–7:00 p.m.; Friday 8:00 a.m.–5:00 p.m.",
        tags="wabash|indiana|healthcare|mental-health|addiction|reentry",
        services="Outpatient therapy|Psychiatric care|Addiction recovery|Crisis stabilization|Primary care|Sliding-fee services",
        county="Wabash",
        served_counties="Wabash",
        coverage="single",
        _source="https://www.bowenhealth.org/wabash-county",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="Learn More Center — Wabash County Adult Education",
        category="education",
        region="North Manchester / Wabash County",
        description=(
            "Learn More Center provides free Indiana High School Equivalency (HSE) classes, career readiness training, "
            "and English language instruction for adults in Wabash County and surrounding north-central Indiana "
            "communities including justice-involved learners seeking credentials for employment after incarceration. "
            "Staff help students enroll, schedule testing, and connect to WorkOne and local employer partners."
        ),
        description_es=(
            "Learn More Center ofrece clases gratuitas de equivalencia de secundaria (HSE) de Indiana, capacitación "
            "de preparación laboral e instrucción en inglés para adultos en el condado Wabash y comunidades circundantes, "
            "incluidos aprendices con antecedentes penales que buscan credenciales para empleo después de la encarcelación."
        ),
        address="603 Bond Street, Suite 12",
        city="North Manchester",
        phone="(260) 330-1461",
        email="",
        website="https://www.in.gov/dwd/career-training-adult-ed/adult-ed/locations/",
        eligibility="Adults 18 and older in Wabash County seeking HSE or career credentials; no criminal-record restrictions stated.",
        eligibility_es="Adultos de 18 años o más en el condado Wabash que buscan HSE o credenciales profesionales; sin restricciones de antecedentes indicadas.",
        notes="Also serves Huntington, Miami, and Grant county ZIP codes; call for orientation and class schedule.",
        notes_es="También sirve códigos postales de Huntington, Miami y Grant; llame para orientación y horario de clases.",
        hours="Contact for class schedules",
        tags="wabash|indiana|education|HSE|adult-ed|reentry",
        services="HSE preparation|Career readiness|English language classes|Testing coordination|WorkOne referrals",
        county="Wabash",
        served_counties="Wabash",
        coverage="single",
        _source="https://www.in.gov/dwd/career-training-adult-ed/adult-ed/locations/",
        _source_type="nonprofit",
        _confidence="high",
    )

    add(
        name="LARA Educational Opportunities — Monticello",
        category="education",
        region="Monticello / White County",
        description=(
            "LARA Educational Opportunities Monticello site provides free Indiana High School Equivalency (HSE) "
            "preparation, career training referrals, and English language classes for White County adults including "
            "justice-involved learners rebuilding credentials after release from incarceration. Students complete online "
            "registration and schedule an orientation appointment before beginning classes at the Monticello learning center."
        ),
        description_es=(
            "El sitio LARA Educational Opportunities en Monticello ofrece preparación gratuita para la equivalencia "
            "de secundaria (HSE) de Indiana, referencias de capacitación profesional y clases de inglés para adultos "
            "del condado White, incluidos aprendices con antecedentes penales que reconstruyen credenciales después "
            "de la encarcelación."
        ),
        address="1017 O'Connor Boulevard",
        city="Monticello",
        phone="(765) 476-2920",
        email="",
        website="https://laralafayette.org/monticello/",
        eligibility="Adults 18 and older in White County seeking HSE or career credentials; no criminal-record restrictions stated.",
        eligibility_es="Adultos de 18 años o más en el condado White que buscan HSE o credenciales profesionales; sin restricciones de antecedentes indicadas.",
        notes="Register online at laralafayette.org; classes Monday/Wednesday evenings and Tuesday/Thursday daytime.",
        notes_es="Regístrese en línea en laralafayette.org; clases lunes/miércoles por la noche y martes/jueves durante el día.",
        hours="Monday and Wednesday 6:00 p.m.–8:00 p.m.; Tuesday and Thursday 9:00 a.m.–7:00 p.m.",
        tags="white|indiana|education|HSE|adult-ed|reentry",
        services="HSE preparation|Career training referrals|English language classes|Online registration|Orientation scheduling",
        county="White",
        served_counties="White",
        coverage="single",
        _source="https://laralafayette.org/monticello/",
        _source_type="nonprofit",
        _confidence="high",
    )

    add(
        name="Gleaners Food Bank — Central Indiana Partner Network",
        category="food-nutrition",
        region="Central Indiana — 21 counties",
        description=(
            "Gleaners Food Bank of Indiana distributes food through partner pantries and mobile distributions across "
            "central Indiana counties where many rural communities have probation and legal aid coverage but limited "
            "local food access. Returning citizens can locate the nearest partner agency by ZIP code through the online "
            "food finder. Food assistance only—not housing, employment, or legal services."
        ),
        description_es=(
            "Gleaners Food Bank of Indiana distribuye alimentos a través de despensas aliadas y distribuciones móviles "
            "en condados del centro de Indiana donde muchas comunidades rurales tienen cobertura de libertad condicional "
            "y asistencia legal pero acceso alimentario local limitado. Los ciudadanos que regresan pueden localizar la "
            "agencia aliada más cercana por código postal en el buscador en línea."
        ),
        address="3737 Waldemar Avenue",
        city="Indianapolis",
        phone="(317) 925-0191",
        email="",
        website="https://www.gleaners.org/find-food/",
        eligibility="Open to Indiana residents needing food assistance through partner agencies; rules vary by pantry.",
        eligibility_es="Abierto a residentes de Indiana que necesitan asistencia alimentaria a través de agencias aliadas; las reglas varían.",
        notes="Use gleaners.org/find-food for the nearest partner pantry by ZIP code before visiting.",
        notes_es="Use gleaners.org/find-food para la despensa aliada más cercana por código postal antes de visitar.",
        hours="Office Monday–Friday; partner pantry hours vary",
        tags="indiana|food-bank|pantry|SNAP|reentry",
        services="Food pantry referrals|Mobile food distribution|Partner agency locator|SNAP information",
        county="Marion",
        served_counties=(
            "Bartholomew|Boone|Brown|Clinton|Decatur|Delaware|Fayette|Franklin|Hamilton|Hancock|Hendricks|"
            "Henry|Johnson|Madison|Marion|Morgan|Putnam|Rush|Shelby|Union|Wayne"
        ),
        coverage="multi",
        _source="https://www.gleaners.org/find-food/",
        _source_type="nonprofit",
        _confidence="high",
    )

    register_tier_a_indiana_gaps(add)


def register_phase3b_ohio(add, entries=None):
    """Rural gap-fill: county JFS via registry + Tier A anchors and thin-county depth."""

    from county_benefits_registry import collect_financial_assistance_counties, register_county_benefits_ohio

    existing_fa = collect_financial_assistance_counties(entries or [])
    register_county_benefits_ohio(add, existing_fa)

    ohio_jfs = [
        ("Noble", "Caldwell", "46049 Marietta Road", "(740) 732-2392", "https://noblefamilies.org", "Caldwell / Noble County",
         "Noble County Job and Family Services is the sole public benefits intake office serving Caldwell and rural Appalachian Ohio, processing Medicaid, SNAP, cash assistance, and OhioMeansJobs connections for returning citizens with no other local provider pinned in the directory."),
        ("Ashland", "Ashland", "15 West Fourth Street", "(419) 282-5000", "https://www.ashlandjfs.org", "Ashland / Ashland County",
         "Ashland County Job and Family Services administers Medicaid, SNAP, and public assistance for Ashland-area residents including justice-involved individuals establishing benefits after release from Ashland County Jail or state facilities."),
        ("Belmont", "St. Clairsville", "310 Fox Shannon Place", "(740) 695-1075", "https://jfs.ohio.gov/about/local-agencies-directory/cdjfs-belmont", "St. Clairsville / Belmont County",
         "Belmont County Job and Family Services provides Medicaid, SNAP, and cash assistance intake for Ohio River valley residents including returning citizens in Belmont County seeking food and health coverage after incarceration."),
        ("Clinton", "Wilmington", "1025 South South Street, Suite 200", "(937) 382-0963", "https://co.clinton.oh.us/departments/JobandFamilyServices", "Wilmington / Clinton County",
         "Clinton County Job and Family Services processes public benefits applications for Wilmington and rural Clinton County residents including justice-involved individuals reconnecting to Medicaid and SNAP after release."),
        ("Crawford", "Bucyrus", "224 Norton Way", "(419) 562-0015", "https://www.crawfordcountyjfs.org", "Bucyrus / Crawford County",
         "Crawford County Job and Family Services is the county benefits office in Bucyrus administering Medicaid, SNAP, and workforce connections for Mid-Ohio returning citizens beyond coalition referral-only rows."),
        ("Defiance", "Defiance", "6879 Evansport Road, Suite A", "(419) 782-3881", "https://jfs.ohio.gov/about/local-agencies-directory/cdjfs-defiance", "Defiance / Defiance County",
         "Defiance County Job and Family Services helps northwest Ohio residents apply for Medicaid, SNAP, and cash assistance including restored citizens establishing benefits after release in Defiance County."),
        ("Erie", "Sandusky", "221 West Parish Street", "(419) 627-4400", "https://www.eriecounty.oh.gov", "Sandusky / Erie County",
         "Erie County Job and Family Services administers public benefits for Sandusky and lakeshore communities including justice-involved residents seeking Medicaid and food assistance after incarceration."),
        ("Gallia", "Gallipolis", "848 Third Avenue", "(740) 446-3222", "https://www.gallianet.net", "Gallipolis / Gallia County",
         "Gallia County Job and Family Services provides SNAP, Medicaid, and cash assistance intake for Appalachian Ohio residents including returning citizens in Gallipolis and surrounding rural communities."),
        ("Guernsey", "Cambridge", "324 Highland Avenue", "(740) 432-2381", "https://www.guernseycountyjfs.org", "Cambridge / Guernsey County",
         "Guernsey County Job and Family Services is the direct-service benefits office in Cambridge helping justice-involved Guernsey County residents apply for Medicaid, SNAP, and OhioMeansJobs support after release."),
        ("Harrison", "Cadiz", "520 North Main Street", "(740) 942-2171", "https://jfs.ohio.gov/about/local-agencies-directory/cdjfs-harrison", "Cadiz / Harrison County",
         "Harrison County Job and Family Services processes Medicaid, SNAP, and public assistance for Cadiz and rural eastern Ohio including returning citizens establishing benefits after incarceration."),
        ("Knox", "Mount Vernon", "117 East High Street, 4th Floor", "(740) 397-7177", "https://www.co.knox.oh.us/jfs/", "Mount Vernon / Knox County",
         "Knox County Job and Family Services administers public benefits and workforce connections for Mount Vernon-area residents including justice-involved individuals seeking Medicaid and SNAP after release."),
        ("Monroe", "Woodsfield", "100 Home Avenue", "(740) 472-1602", "https://www.monroecountyohio.com/departments/job_and_family_services/index.php", "Woodsfield / Monroe County",
         "Monroe County Job and Family Services is the county benefits intake office in Woodsfield serving Appalachian Ohio including returning citizens in Ohio's least-populated counties seeking food and health coverage."),
        ("Paulding", "Paulding", "252 Dooley Drive", "(419) 399-3756", "https://jfs.ohio.gov/about/local-agencies-directory/cdjfs-paulding", "Paulding / Paulding County",
         "Paulding County Job and Family Services helps northwest Ohio residents apply for Medicaid, SNAP, and cash assistance including restored citizens in Paulding County establishing public benefits after release."),
        ("Seneca", "Tiffin", "900 East County Road 20", "(419) 447-5011", "https://jfs.ohio.gov/about/local-agencies-directory/cdjfs-seneca", "Tiffin / Seneca County",
         "Seneca County Job and Family Services administers Medicaid, SNAP, and public assistance for Tiffin and rural Seneca County including justice-involved residents reconnecting to benefits after incarceration."),
        ("Tuscarawas", "New Philadelphia", "389 16th Street SW", "(330) 339-7791", "https://www.tcjfs.org", "New Philadelphia / Tuscarawas County",
         "Tuscarawas County Job and Family Services provides direct benefits intake in New Philadelphia for Medicaid, SNAP, and workforce services beyond legal-aid-only coverage for returning citizens."),
        ("Van Wert", "Van Wert", "114 East Main Street", "(419) 238-5430", "https://jfs.ohio.gov/about/local-agencies-directory/cdjfs-van-wert", "Van Wert / Van Wert County",
         "Van Wert County Job and Family Services processes public benefits for northwest Ohio residents including justice-involved individuals in Van Wert County seeking Medicaid and food assistance after release."),
        ("Washington", "Marietta", "1115 Gilman Avenue", "(740) 373-5513", "https://www.washingtongov.org/", "Marietta / Washington County",
         "Washington County Job and Family Services administers Medicaid, SNAP, and cash assistance for Marietta and Ohio River communities including returning citizens establishing benefits in southeast Ohio."),
        ("Williams", "Bryan", "117 West Butler Street", "(419) 636-6725", "https://jfs.ohio.gov/about/local-agencies-directory/cdjfs-williams", "Bryan / Williams County",
         "Williams County Job and Family Services helps northwest Ohio residents apply for Medicaid, SNAP, and public assistance including restored citizens in Bryan and Williams County after incarceration."),
        ("Wyandot", "Upper Sandusky", "120 East Johnson Street", "(419) 617-4230", "https://www.co.wyandot.oh.us/jfs/index.htm", "Upper Sandusky / Wyandot County",
         "Wyandot County Job and Family Services is the county benefits office in Upper Sandusky providing Medicaid, SNAP, and OhioMeansJobs connections for justice-involved Wyandot County residents after release."),
    ]

    for county, city, address, phone, website, region, desc_en in ohio_jfs:
        if county in existing_fa:
            continue
        desc_es = (
            desc_en.replace("Job and Family Services", "Job and Family Services del condado")
            .replace("Medicaid, SNAP", "Medicaid, SNAP")
            .replace("returning citizens", "ciudadanos que regresan")
            .replace("justice-involved", "personas con antecedentes penales")
            .replace("including", "incluidos")
        )
        if "del condado del condado" in desc_es:
            desc_es = desc_es.replace("del condado del condado", "del condado")
        add(**_jfs_oh(county, city, address, phone, website, region, desc_en, desc_es))
        existing_fa.add(county)

    add(
        **_jfs_oh(
            "Adams",
            "West Union",
            "912 Robinson Road",
            "(937) 544-2921",
            "https://www.adamscountyoh.gov/departments/job_family_services/index.php",
            "West Union / Adams County",
            (
                "Adams County Job and Family Services in West Union administers Medicaid, SNAP, Ohio Works First "
                "cash assistance, and child care subsidies for Appalachian Ohio residents including returning "
                "citizens from Adams County Jail establishing food and health coverage after release. Staff assist "
                "with benefits.ohio.gov applications and OhioMeansJobs connections for fair-chance employment."
            ),
            (
                "Adams County Job and Family Services en West Union administra Medicaid, SNAP, asistencia en "
                "efectivo Ohio Works First y subsidios de cuidado infantil para residentes del condado Adams, "
                "incluidos ciudadanos que regresan de la cárcel del condado que establecen cobertura alimentaria "
                "y de salud después de la liberación."
            ),
        )
    )
    add(
        name="OhioMeansJobs — Adams County",
        category="employment",
        region="West Union / Adams County",
        description=(
            "OhioMeansJobs Adams County connects job seekers in West Union and rural Adams County to resume "
            "writing, interview coaching, job search tools, and WIOA training referrals through the county "
            "American Job Center network. Justice-involved job seekers can access fair-chance employment "
            "resources and OhioMeansJobs account support co-located with Adams County Job and Family Services."
        ),
        description_es=(
            "OhioMeansJobs del condado Adams conecta a buscadores de empleo en West Union y el condado rural "
            "Adams con redacción de currículum, coaching de entrevistas, herramientas de búsqueda y referencias "
            "WIOA a través de la red de Centros de Empleo Americanos. Personas con antecedentes penales pueden "
            "acceder a recursos de empleo justo junto con Adams County Job and Family Services."
        ),
        address="912 Robinson Road",
        city="West Union",
        phone="(937) 544-2921",
        email="",
        website="https://jfs.ohio.gov/about/local-agencies-directory/omj-adams",
        eligibility="Open to Adams County job seekers including justice-involved individuals; core services are free.",
        eligibility_es="Abierto a buscadores de empleo del condado Adams, incluidas personas con antecedentes penales; servicios básicos gratuitos.",
        notes="Co-located with Adams County JFS; call ahead for AJC specialist availability.",
        notes_es="Ubicado junto a Adams County JFS; llame con anticipación para disponibilidad del especialista AJC.",
        hours="Monday–Friday, 7:30 a.m.–4:30 p.m.",
        tags="adams|ohio|employment|american-job-center|workforce|reentry",
        services="Job search assistance|Resume writing|Interview coaching|WIOA training referrals|Fair-chance employment navigation",
        county="Adams",
        served_counties="Adams",
        coverage="single",
        _source="https://jfs.ohio.gov/about/local-agencies-directory/omj-adams",
        _source_type="government",
        _confidence="high",
    )

    add(
        name="OhioMeansJobs — Noble County",
        category="employment",
        region="Caldwell / Noble County",
        description=(
            "OhioMeansJobs Noble County is the local American Job Center co-located with Noble County Job and "
            "Family Services in Caldwell, providing career coaching, resume writing, job search assistance, and "
            "WIOA training referrals for job seekers including ex-offenders seeking fair-chance employment after "
            "release. Veterans employment representatives available by appointment. Employers can access recruitment "
            "and pre-screening services through the same Caldwell workforce office."
        ),
        description_es=(
            "OhioMeansJobs del condado Noble es el Centro de Empleo Americano local en Caldwell que ofrece coaching "
            "de carrera, redacción de currículum, búsqueda de empleo y referencias de capacitación WIOA para "
            "buscadores de empleo, incluidos exdelincuentes que buscan empleo justo después de la liberación. "
            "Representantes de empleo para veteranos disponibles con cita previa."
        ),
        address="46049 Marietta Road",
        city="Caldwell",
        phone="(740) 732-2392",
        email="noblecountyjobsetc@yahoo.com",
        website="https://ohiomeansjobs.com/noble",
        eligibility="Ohio residents seeking employment services; ex-offender job placement and resume services available per center listing.",
        eligibility_es="Residentes de Ohio que buscan servicios de empleo; colocación laboral y currículum para exdelincuentes disponibles según listado del centro.",
        notes="Co-located with Noble County JFS; Mon–Thu 6:00 a.m.–4:00 p.m.; WIOA and CCMEP career advancement programs available.",
        notes_es="Ubicado junto a JFS del condado Noble; lun–jue 6:00 a.m.–4:00 p.m.; programas WIOA y CCMEP disponibles.",
        hours="Monday–Thursday, 6:00 a.m.–4:00 p.m.",
        tags="noble|ohio|employment|OhioMeansJobs|reentry|ex-offender",
        services="Job search assistance|Resume writing|Ex-offender job placement|WIOA training referrals|Veterans employment services|Employer recruitment support",
        county="Noble",
        served_counties="Noble",
        coverage="single",
        _source="https://jfs.ohio.gov/about/local-agencies-directory/omj-noble",
        _source_type="government",
        _confidence="high",
    )

    add(
        name="Akron-Canton Regional Foodbank — Partner Agency Network",
        category="food-nutrition",
        region="Northeast Ohio — 10 counties",
        description=(
            "Akron-Canton Regional Foodbank supplies partner pantries and mobile distributions across northeast Ohio "
            "counties where many rural communities have legal aid and JFS coverage but need a third Tier A food "
            "resource. Returning citizens can locate the nearest partner pantry by ZIP code through the online food "
            "finder. Food assistance only—not housing, employment, or legal services."
        ),
        description_es=(
            "Akron-Canton Regional Foodbank abastece despensas aliadas y distribuciones móviles en condados del "
            "noreste de Ohio donde muchas comunidades rurales tienen asistencia legal y JFS pero necesitan un tercer "
            "recurso alimentario Tier A. Los ciudadanos que regresan pueden localizar la despensa aliada más cercana "
            "por código postal en el buscador en línea."
        ),
        address="350 Opportunity Parkway",
        city="Akron",
        phone="(330) 535-6900",
        email="",
        website="https://www.akroncantonfoodbank.org/find-help/get-food",
        eligibility="Open to northeast Ohio residents needing food assistance through partner agencies.",
        eligibility_es="Abierto a residentes del noreste de Ohio que necesitan asistencia alimentaria a través de agencias aliadas.",
        notes="Use akroncantonfoodbank.org food finder for nearest partner site by ZIP code.",
        notes_es="Use el buscador de alimentos de akroncantonfoodbank.org para el sitio aliado más cercano por código postal.",
        hours="Office Monday–Friday; partner pantry hours vary",
        tags="northeast-ohio|food-bank|pantry|reentry",
        services="Food pantry referrals|Mobile food distribution|Partner agency locator|SNAP information",
        county="Summit",
        served_counties="Carroll|Columbiana|Holmes|Mahoning|Medina|Portage|Stark|Summit|Tuscarawas|Wayne",
        coverage="multi",
        _source="https://www.akroncantonfoodbank.org/find-help/get-food",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="Toledo Northwestern Ohio Food Bank — Partner Pantry Network",
        category="food-nutrition",
        region="Northwest Ohio — 11 counties",
        description=(
            "Toledo Northwestern Ohio Food Bank connects low-income residents across northwest Ohio to partner "
            "pantries and mobile distributions in counties where county JFS offices provide benefits intake but local "
            "food depth is thin. Returning citizens can use the online pantry locator to find the nearest distribution "
            "site. Food assistance only—not direct housing or employment services."
        ),
        description_es=(
            "Toledo Northwestern Ohio Food Bank conecta a residentes de bajos ingresos del noroeste de Ohio con "
            "despensas aliadas y distribuciones móviles en condados donde las oficinas JFS del condado ofrecen "
            "admisión de beneficios pero la profundidad alimentaria local es limitada. Los ciudadanos que regresan "
            "pueden usar el localizador en línea para encontrar el sitio de distribución más cercano."
        ),
        address="24 West Woodruff Avenue",
        city="Toledo",
        phone="(419) 242-5000",
        email="",
        website="https://toledofoodbank.org/get-help/",
        eligibility="Open to northwest Ohio residents needing food assistance through partner agencies.",
        eligibility_es="Abierto a residentes del noroeste de Ohio que necesitan asistencia alimentaria a través de agencias aliadas.",
        notes="Partner pantry hours vary; use toledofoodbank.org locator before visiting.",
        notes_es="Los horarios de despensas aliadas varían; use el localizador de toledofoodbank.org antes de visitar.",
        hours="Office Monday–Friday; partner sites vary",
        tags="northwest-ohio|food-bank|pantry|reentry",
        services="Food pantry referrals|Mobile food distribution|Partner agency locator|SNAP application information",
        county="Lucas",
        served_counties="Defiance|Erie|Fulton|Henry|Huron|Lucas|Ottawa|Paulding|Sandusky|Seneca|Williams",
        coverage="multi",
        _source="https://toledofoodbank.org/get-help/",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="HAPCAP Southeast Ohio Foodbank — Partner Network",
        category="food-nutrition",
        region="Southeast Ohio — 6 counties",
        description=(
            "HAPCAP Southeast Ohio Foodbank distributes food through partner pantries across Appalachian Ohio counties "
            "where legal aid and county JFS provide two Tier A categories but food access remains a gap. Returning "
            "citizens can locate partner agencies through HAPCAP's online food assistance directory. Food and nutrition "
            "support only—not housing, employment, or legal representation."
        ),
        description_es=(
            "HAPCAP Southeast Ohio Foodbank distribuye alimentos a través de despensas aliadas en condados "
            "apalaches de Ohio donde la asistencia legal y JFS del condado cubren dos categorías Tier A pero falta "
            "acceso alimentario. Los ciudadanos que regresan pueden localizar agencias aliadas en el directorio en "
            "línea de HAPCAP."
        ),
        address="3 Cardaras Drive",
        city="Athens",
        phone="(740) 594-4496",
        email="",
        website="https://www.hapcap.org/food-assistance",
        eligibility="Open to southeast Ohio residents needing food assistance through partner agencies.",
        eligibility_es="Abierto a residentes del sureste de Ohio que necesitan asistencia alimentaria a través de agencias aliadas.",
        notes="Use hapcap.org food assistance page for partner pantry locations by county.",
        notes_es="Use la página de asistencia alimentaria de hapcap.org para ubicaciones de despensas aliadas por condado.",
        hours="Office Monday–Friday; partner pantry hours vary",
        tags="southeast-ohio|food-bank|appalachian|reentry",
        services="Food pantry referrals|Mobile food distribution|Partner agency locator|SNAP information",
        county="Athens",
        served_counties="Athens|Hocking|Meigs|Morgan|Perry|Vinton",
        coverage="multi",
        _source="https://www.hapcap.org/food-assistance",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="Ohio Adult Parole Authority — Southeast Region Field Services",
        category="probation-parole",
        region="Southeast Ohio — 12 counties",
        description=(
            "Ohio Adult Parole Authority southeast region field offices supervise state parole and community control "
            "for justice-involved individuals in Appalachian and Ohio River valley counties. Parole officers connect "
            "supervisees to county Job and Family Services, OhioMeansJobs centers, and regional treatment and housing "
            "partners. Contact for reporting requirements and supervision compliance—not emergency reentry navigation."
        ),
        description_es=(
            "Las oficinas de campo de la región sureste de la Autoridad de Libertad Condicional de Ohio supervisan "
            "libertad condicional estatal y control comunitario para personas con antecedentes penales en condados "
            "apalaches y del valle del Ohio. Los oficiales conectan a supervisados con JFS del condado, OhioMeansJobs "
            "y aliados regionales de tratamiento y vivienda. Contacte para requisitos de reporte, no para navegación "
            "de crisis."
        ),
        address="770 West Broad Street",
        city="Columbus",
        phone="(614) 752-1161",
        email="",
        website="https://drc.ohio.gov/about-us/divisions-and-offices/adult-parole-authority",
        eligibility="Individuals under Ohio state parole or post-release control in listed southeast Ohio counties.",
        eligibility_es="Personas bajo libertad condicional estatal o control posterior a la liberación de Ohio en los condados listados.",
        notes="Field office locations vary by supervisee assignment; confirm reporting site with assigned officer.",
        notes_es="Las ubicaciones de oficinas de campo varían según la asignación; confirme el sitio de reporte con su oficial.",
        hours="Monday–Friday business hours",
        tags="southeast-ohio|parole|probation|ODRC|reentry",
        services="Parole supervision|Community control|Reporting compliance|Workforce referrals|Treatment referrals",
        county="Washington",
        served_counties=(
            "Adams|Athens|Belmont|Gallia|Guernsey|Harrison|Jackson|Lawrence|Meigs|Monroe|Morgan|Washington"
        ),
        coverage="multi",
        _source="https://drc.ohio.gov/about-us/divisions-and-offices/adult-parole-authority",
        _source_type="government",
        _confidence="high",
    )

    ohio_omj_rural = [
        ("Coshocton", "Coshocton", "724 South Seventh Street", "(740) 622-1366", "https://jfs.ohio.gov/about/local-agencies-directory/omj-coshocton"),
        ("Delaware", "Delaware", "844 South Sandusky Street", "(740) 833-2312", "https://jfs.ohio.gov/about/local-agencies-directory/omj-delaware"),
        ("Fayette", "Washington Court House", "133 South Main Street", "(740) 335-7282", "https://jfs.ohio.gov/about/local-agencies-directory/omj-fayette"),
        ("Fulton", "Wauseon", "604 South Shoop Avenue", "(419) 337-5015", "https://jfs.ohio.gov/about/local-agencies-directory/omj-fulton"),
        ("Highland", "Hillsboro", "1575 North High Street", "(937) 393-1925", "https://jfs.ohio.gov/about/local-agencies-directory/omj-highland"),
        ("Hocking", "Logan", "3800 Colony Drive", "(740) 385-6811", "https://jfs.ohio.gov/about/local-agencies-directory/omj-hocking"),
        ("Jackson", "Jackson", "990 East Main Street", "(740) 286-4151", "https://jfs.ohio.gov/about/local-agencies-directory/omj-jackson"),
        ("Morrow", "Mount Gilead", "619 West Marion Road", "(419) 947-9115", "https://jfs.ohio.gov/about/local-agencies-directory/omj-morrow"),
        ("Perry", "New Lexington", "833 North Main Street", "(740) 342-3231", "https://jfs.ohio.gov/about/local-agencies-directory/omj-perry"),
        ("Pike", "Waverly", "941 Market Street", "(740) 947-9115", "https://jfs.ohio.gov/about/local-agencies-directory/omj-pike"),
        ("Ross", "Chillicothe", "475 Western Avenue", "(740) 702-7220", "https://jfs.ohio.gov/about/local-agencies-directory/omj-ross"),
        ("Scioto", "Portsmouth", "721 Eighth Street", "(740) 354-7791", "https://jfs.ohio.gov/about/local-agencies-directory/omj-scioto"),
        ("Vinton", "McArthur", "325 West High Street", "(740) 596-5242", "https://jfs.ohio.gov/about/local-agencies-directory/omj-vinton"),
    ]
    for county, city, address, phone, website in ohio_omj_rural:
        add(
            name=f"OhioMeansJobs — {county} County",
            category="employment",
            region=f"{city} / {county} County",
            description=(
                f"OhioMeansJobs {county} County is the local American Job Center connecting rural Ohio job seekers "
                f"including justice-involved residents to resume writing, interview coaching, job search tools, and "
                f"WIOA training referrals. Staff assist with fair-chance employment navigation and OhioMeansJobs "
                f"account setup co-located with or near {county} County Job and Family Services."
            ),
            description_es=(
                f"OhioMeansJobs del condado {county} es el Centro de Empleo Americano local que conecta a buscadores "
                f"de empleo rurales de Ohio, incluidos residentes con antecedentes penales, con redacción de currículum, "
                f"coaching de entrevistas, herramientas de búsqueda y referencias WIOA. El personal ayuda con navegación "
                f"de empleo justo y configuración de cuenta OhioMeansJobs."
            ),
            address=address,
            city=city,
            phone=phone,
            email="",
            website=website,
            eligibility=f"Open to {county} County job seekers including justice-involved individuals; core services are free.",
            eligibility_es=f"Abierto a buscadores de empleo del condado {county}, incluidas personas con antecedentes penales; servicios básicos gratuitos.",
            notes="Call ahead for AJC specialist availability; unemployment claims filed online at OhioMeansJobs.com.",
            notes_es="Llame con anticipación para disponibilidad del especialista AJC; solicitudes de desempleo en OhioMeansJobs.com.",
            hours="Monday–Friday, 7:30 a.m.–4:30 p.m.",
            tags=f"{county.lower()}|ohio|employment|OhioMeansJobs|reentry",
            services="Job search assistance|Resume writing|Interview coaching|WIOA training referrals|Fair-chance employment navigation",
            county=county,
            served_counties=county,
            coverage="single",
            _source=website,
            _source_type="government",
            _confidence="high",
        )

    from tier_a_anchors import register_ohio_tier_a_anchors

    register_ohio_tier_a_anchors(add, _jfs_oh, existing_fa)


def register_phase3b_tennessee(add, entries=None):
    """Phase 3b: TDHS Family Assistance (registry) + Tier A anchors and thin-county depth."""

    from county_benefits_registry import collect_financial_assistance_counties, register_county_benefits_tennessee

    existing_fa = collect_financial_assistance_counties(entries or [])
    register_county_benefits_tennessee(add, existing_fa)

    tn_dhs = [
        ("Benton", "Camden", "272 Highway 641 North", "(731) 593-6360", "Camden / Benton County",
         "Benton County Department of Human Services Family Assistance office in Camden processes SNAP, Families First, Medicaid, and TennCare applications for West Tennessee residents including returning citizens released from Benton County Jail seeking food and health coverage."),
        ("Campbell", "LaFollette", "2221 Jacksboro Pike, Suite C-19A, Woodson's Mall", "(423) 566-9639", "LaFollette / Campbell County",
         "Campbell County DHS Family Assistance office in LaFollette helps northeast Tennessee residents apply for SNAP, Medicaid, TennCare, and Families First including justice-involved individuals reestablishing benefits after incarceration in Appalachian Tennessee."),
        ("Carroll", "Huntingdon", "20810 Main Street East", "(731) 352-7941", "Huntingdon / Carroll County",
         "Carroll County DHS Family Assistance office in Huntingdon administers SNAP, Medicaid, and Families First for rural West Tennessee including returning citizens in Carroll County establishing public benefits after release."),
        ("Claiborne", "Tazewell", "310 Court Street", "(423) 626-7285", "Tazewell / Claiborne County",
         "Claiborne County DHS Family Assistance office in Tazewell processes SNAP, TennCare, and Families First applications for northeast Tennessee residents including justice-involved individuals seeking food and health coverage after incarceration."),
        ("Dyer", "Dyersburg", "1979 St. John Avenue, Suite E", "(731) 286-8305", "Dyersburg / Dyer County",
         "Dyer County DHS Family Assistance office in Dyersburg helps northwest Tennessee residents apply for SNAP, Medicaid, TennCare, and child care certificates including returning citizens reconnecting to benefits after release from Dyer County Jail."),
        ("Gibson", "Trenton", "2205 Highway 45 Bypass South", "(731) 824-4302", "Trenton / Gibson County",
         "Gibson County DHS Family Assistance office in Trenton administers SNAP, Families First, and TennCare for West Tennessee including justice-involved Gibson County residents establishing food and health benefits after incarceration."),
        ("Henry", "Paris", "1023 Mineral Wells Avenue, Suite F", "(731) 644-7350", "Paris / Henry County",
         "Henry County DHS Family Assistance office in Paris processes public benefits for northwest Tennessee including returning citizens in Henry County seeking SNAP, Medicaid, and Families First after release from local jail or state custody."),
        ("Houston", "Erin", "21 Store Front Drive", "(931) 289-4105", "Erin / Houston County",
         "Houston County DHS Family Assistance office in Erin serves rural Middle Tennessee including justice-involved residents applying for SNAP, TennCare, and Families First after incarceration in one of Tennessee's smallest counties."),
        ("Humphreys", "Waverly", "1203 Highway 70 West", "(931) 296-4227", "Waverly / Humphreys County",
         "Humphreys County DHS Family Assistance office in Waverly helps residents apply for SNAP, Medicaid, TennCare, and child care assistance including returning citizens reestablishing benefits after release in the Tennessee River valley."),
        ("Lake", "Tiptonville", "660 Carl Perkins Parkway", "(731) 253-7716", "Tiptonville / Lake County",
         "Lake County DHS Family Assistance office in Tiptonville administers SNAP, Families First, and TennCare for Tennessee's northwest corner including justice-involved Lake County residents seeking food and health coverage after incarceration."),
        ("Morgan", "Wartburg", "1326 Knoxville Highway, Suite 1", "(423) 346-6237", "Wartburg / Morgan County",
         "Morgan County DHS Family Assistance office in Wartburg processes SNAP, Medicaid, and Families First for rural East Tennessee including returning citizens in Morgan County establishing public benefits after release from local custody."),
        ("Obion", "Union City", "700 Sherrill Street", "(731) 884-2603", "Union City / Obion County",
         "Obion County DHS Family Assistance office in Union City helps northwest Tennessee residents apply for SNAP, TennCare, and Families First including justice-involved Obion County residents reconnecting to food and health benefits after incarceration."),
        ("Polk", "Benton", "240 Cherokee Circle", "(423) 338-5332", "Benton / Polk County",
         "Polk County DHS Family Assistance office in Benton administers SNAP, Medicaid, TennCare, and Families First for southeast Tennessee including returning citizens in Polk County seeking public benefits after release from local jail."),
        ("Scott", "Huntsville", "104 Fire Hall Drive", "(423) 663-2821", "Huntsville / Scott County",
         "Scott County DHS Family Assistance office in Huntsville processes SNAP, Families First, and TennCare for rural East Tennessee including justice-involved Scott County residents establishing food and health coverage after incarceration."),
        ("Stewart", "Dover", "1011 Spring Street", "(931) 232-5304", "Dover / Stewart County",
         "Stewart County DHS Family Assistance office in Dover helps Fort Campbell corridor and rural Middle Tennessee residents apply for SNAP, Medicaid, and Families First including returning citizens reestablishing benefits after release."),
        ("Union", "Maynardville", "1403 Main Street", "(865) 992-5802", "Maynardville / Union County",
         "Union County DHS Family Assistance office in Maynardville administers SNAP, TennCare, and Families First for northeast Tennessee including justice-involved Union County residents seeking food and health benefits after incarceration."),
        ("Weakley", "Dresden", "8616 Highway 22", "(731) 364-3128", "Dresden / Weakley County",
         "Weakley County DHS Family Assistance office in Dresden processes SNAP, Medicaid, TennCare, and Families First for northwest Tennessee including returning citizens in Weakley County establishing public benefits after release from local custody."),
    ]

    for county, city, address, phone, region, desc_en in tn_dhs:
        if county in existing_fa:
            continue
        desc_es = _dhs_desc_es(county, city)
        add(**_dhs_tn(county, city, address, phone, region, desc_en, desc_es))
        existing_fa.add(county)

    # TDOC West Tennessee field offices covering additional uncovered counties
    add(
        name="TDOC Community Supervision — District 61 (Dresden)",
        category="probation-parole",
        region="West Tennessee — Gibson and Weakley",
        description=(
            "TDOC District 61 field office in Dresden supervises probation and parole for Gibson and Weakley County "
            "residents including returning citizens reporting after release from West Tennessee facilities. Officers "
            "connect supervisees to DHS benefits offices, American Job Centers, and regional reentry partners in "
            "northwest Tennessee. Contact for reporting requirements and supervision compliance—not emergency services."
        ),
        description_es=(
            "La oficina de campo del Distrito 61 del TDOC en Dresden supervisa libertad probatoria y condicional para "
            "residentes de los condados Gibson y Weakley, incluidos ciudadanos que reportan después de la liberación. "
            "Los oficiales conectan a supervisados con oficinas de beneficios DHS y aliados de reinserción regional. "
            "Contacte para requisitos de reporte, no para servicios de emergencia."
        ),
        address="8593 Highway 22",
        city="Dresden",
        phone="(731) 364-3147",
        email="",
        website="https://www.tn.gov/correction/cs/field-office-directory.html",
        eligibility="Individuals under Tennessee probation or parole supervision in Gibson and Weakley counties.",
        eligibility_es="Personas bajo supervisión de libertad probatoria o condicional en los condados Gibson y Weakley.",
        notes="District 61 also serves Benton, Carroll, Crockett, Decatur, Dyer, Hardin, Henderson, Henry, Lake, Lauderdale, and Obion through satellite offices.",
        notes_es="El Distrito 61 también sirve a Benton, Carroll, Crockett, Decatur, Dyer, Hardin, Henderson, Henry, Lake, Lauderdale y Obion a través de oficinas satélite.",
        hours="Monday–Friday business hours",
        tags="gibson|weakley|tennessee|probation|parole|TDOC|reentry",
        services="Probation and parole supervision|Reporting compliance|DRC referrals|Employment specialist referrals|Reentry partner connections",
        county="Weakley",
        served_counties="Gibson|Weakley",
        coverage="multi",
        _source="https://www.tn.gov/correction/cs/field-office-directory.html",
        _source_type="government",
        _confidence="high",
    )
    add(
        name="TDOC Community Supervision — District 61 (Dyersburg)",
        category="probation-parole",
        region="West Tennessee — Dyer, Lake, and Lauderdale",
        description=(
            "TDOC District 61 Dyersburg field office supervises probation and parole for Dyer, Lake, and Lauderdale "
            "County residents including returning citizens reporting after release from northwest Tennessee jails and "
            "state facilities. Officers connect supervisees to county DHS benefits offices, workforce centers, and "
            "regional food and treatment partners. Contact for reporting requirements—not emergency reentry navigation."
        ),
        description_es=(
            "La oficina de campo del TDOC en Dyersburg del Distrito 61 supervisa libertad probatoria y condicional "
            "para residentes de los condados Dyer, Lake y Lauderdale, incluidos ciudadanos que reportan después de "
            "la liberación. Los oficiales conectan a supervisados con oficinas DHS del condado y centros de empleo. "
            "Contacte para requisitos de reporte, no para navegación de crisis de reinserción."
        ),
        address="1979 St. John Avenue",
        city="Dyersburg",
        phone="(731) 288-7910",
        email="",
        website="https://www.tn.gov/correction/cs/field-office-directory.html",
        eligibility="Individuals under Tennessee probation or parole supervision in Dyer, Lake, or Lauderdale counties.",
        eligibility_es="Personas bajo supervisión de libertad probatoria o condicional en los condados Dyer, Lake o Lauderdale.",
        notes="Alternative phone (731) 288-7514; co-located near Dyer County DHS Family Assistance office.",
        notes_es="Teléfono alternativo (731) 288-7514; ubicado cerca de la oficina de Asistencia Familiar DHS del condado Dyer.",
        hours="Monday–Friday business hours",
        tags="dyer|lake|lauderdale|tennessee|probation|parole|TDOC|reentry",
        services="Probation and parole supervision|Reporting compliance|Benefits office referrals|Workforce connections|Treatment referrals",
        county="Dyer",
        served_counties="Dyer|Lake|Lauderdale",
        coverage="multi",
        _source="https://www.tn.gov/correction/cs/field-office-directory.html",
        _source_type="government",
        _confidence="high",
    )
    add(
        name="TDOC Community Supervision — District 61 (Huntingdon)",
        category="probation-parole",
        region="West Tennessee — Carroll County",
        description=(
            "TDOC District 61 Huntingdon field office at the Carroll County courthouse supervises probation and "
            "parole for Carroll County residents including returning citizens reporting after release from West "
            "Tennessee correctional facilities. Officers connect supervisees to county DHS benefits intake, American "
            "Job Centers, and regional reentry partners. Contact for reporting requirements—not emergency services."
        ),
        description_es=(
            "La oficina de campo del TDOC en Huntingdon del Distrito 61 supervisa libertad probatoria y condicional "
            "para residentes del condado Carroll, incluidos ciudadanos que reportan después de la liberación de "
            "instalaciones correccionales del oeste de Tennessee. Los oficiales conectan a supervisados con admisión "
            "de beneficios DHS del condado y centros de empleo."
        ),
        address="99 Court Square, Suite B-02",
        city="Huntingdon",
        phone="(731) 986-5062",
        email="",
        website="https://www.tn.gov/correction/cs/field-office-directory.html",
        eligibility="Individuals under Tennessee probation or parole supervision in Carroll County.",
        eligibility_es="Personas bajo supervisión de libertad probatoria o condicional en el condado Carroll.",
        notes="District 61 satellite office; also serves Benton, Decatur, Hardin, and Henderson counties from regional offices.",
        notes_es="Oficina satélite del Distrito 61; también sirve a los condados Benton, Decatur, Hardin y Henderson desde oficinas regionales.",
        hours="Monday–Friday business hours",
        tags="carroll|tennessee|probation|parole|TDOC|reentry",
        services="Probation and parole supervision|Reporting compliance|DHS referrals|Employment connections|Reentry partner referrals",
        county="Carroll",
        served_counties="Carroll",
        coverage="single",
        _source="https://www.tn.gov/correction/cs/field-office-directory.html",
        _source_type="government",
        _confidence="high",
    )

    add(
        name="Second Harvest Food Bank of East Tennessee — Partner Agency Network",
        category="food-nutrition",
        region="East Tennessee — 18 counties",
        description=(
            "Second Harvest Food Bank of East Tennessee distributes food through partner pantries and meal "
            "programs across 18 counties including many rural East Tennessee communities with thin local "
            "reentry directories. Returning citizens can locate the nearest partner pantry by ZIP code through "
            "the online food finder. Not an emergency shelter or cash assistance program—food and nutrition "
            "support only."
        ),
        description_es=(
            "Second Harvest Food Bank of East Tennessee distribuye alimentos a través de despensas aliadas en "
            "18 condados del este de Tennessee, incluidas comunidades rurales con pocos recursos locales de "
            "reinserción. Los ciudadanos que regresan pueden localizar la despensa aliada más cercana por "
            "código postal en el buscador en línea."
        ),
        address="136 Harvest Lane",
        city="Maryville",
        phone="(865) 521-0000",
        email="",
        website="https://secondharvestetn.org/find-food/",
        eligibility="Open to East Tennessee residents needing food assistance; partner pantry rules vary.",
        eligibility_es="Abierto a residentes del este de Tennessee que necesitan asistencia alimentaria; las reglas de despensas aliadas varían.",
        notes="Use the online food finder for the nearest partner agency by ZIP code.",
        notes_es="Use el buscador en línea para la agencia aliada más cercana por código postal.",
        hours="Office Monday–Friday; partner pantry hours vary",
        tags="east-tennessee|food-bank|SNAP|pantry|reentry",
        services="Food pantry referrals|Mobile food distribution|SNAP application assistance|Partner agency locator",
        county="Blount",
        served_counties=(
            "Bedford|Bledsoe|Blount|Bradley|Campbell|Claiborne|Cocke|Coffee|Franklin|Grundy|Hamblen|"
            "Marion|McMinn|Meigs|Morgan|Monroe|Polk|Rhea|Scott|Sequatchie|Stewart"
        ),
        coverage="multi",
        _source="https://secondharvestetn.org/find-food/",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="Mid-South Food Bank — Partner Pantry Network",
        category="food-nutrition",
        region="West Tennessee — 20 counties",
        description=(
            "Mid-South Food Bank supplies partner food pantries and mobile distributions across west Tennessee "
            "counties including many rural communities where county DHS is the only local pin. Returning citizens "
            "can use the online pantry locator to find the nearest distribution site. Food assistance only—not "
            "housing, employment, or legal services."
        ),
        description_es=(
            "Mid-South Food Bank abastece despensas aliadas y distribuciones móviles en condados del oeste de "
            "Tennessee, incluidas comunidades rurales donde DHS del condado es el único recurso local. Los "
            "ciudadanos que regresan pueden usar el localizador en línea para encontrar el sitio más cercano."
        ),
        address="3865 South Perkins Road",
        city="Memphis",
        phone="(901) 527-1511",
        email="",
        website="https://www.midsouthfoodbank.org/find-food",
        eligibility="Open to west Tennessee residents needing food assistance through partner agencies.",
        eligibility_es="Abierto a residentes del oeste de Tennessee que necesitan asistencia alimentaria a través de agencias aliadas.",
        notes="Partner pantry hours and eligibility vary by site; use online locator before visiting.",
        notes_es="Horarios y elegibilidad varían por sitio; use el localizador en línea antes de visitar.",
        hours="Office Monday–Friday; partner sites vary",
        tags="west-tennessee|food-bank|pantry|SNAP|reentry",
        services="Food pantry referrals|Mobile food distribution|Partner agency locator|SNAP information",
        county="Shelby",
        served_counties=(
            "Benton|Carroll|Chester|Crockett|Decatur|Dyer|Fayette|Gibson|Hardeman|Hardin|Haywood|"
            "Henderson|Henry|Houston|Lake|Lauderdale|Madison|McNairy|Obion|Tipton|Weakley"
        ),
        coverage="multi",
        _source="https://www.midsouthfoodbank.org/find-food",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="American Job Center — Rural Middle Tennessee Workforce Network",
        category="employment",
        region="Middle Tennessee — 12 counties",
        description=(
            "Tennessee American Job Centers provide free job search assistance, resume help, interview coaching, "
            "and training referrals through the statewide Jobs4TN network. This regional entry covers AJC access "
            "for rural Middle Tennessee counties where workforce services are often co-located with county "
            "DHS or career centers. Justice-involved job seekers can request fair-chance employer connections."
        ),
        description_es=(
            "Los Centros de Empleo Americanos de Tennessee ofrecen asistencia gratuita de búsqueda de empleo, "
            "currículum, entrevistas y referencias de capacitación a través de la red Jobs4TN. Esta entrada "
            "regional cubre acceso AJC para condados rurales del centro de Tennessee donde los servicios "
            "laborales suelen estar junto a DHS del condado."
        ),
        address="",
        city="Nashville",
        phone="(844) 224-5818",
        email="",
        website="https://www.jobs4tn.gov/",
        eligibility="Open to Tennessee job seekers including justice-involved individuals; core AJC services are free.",
        eligibility_es="Abierto a buscadores de empleo de Tennessee, incluidas personas con antecedentes penales; servicios básicos gratuitos.",
        notes="Call Jobs4TN or visit jobs4tn.gov to locate the nearest AJC by county.",
        notes_es="Llame a Jobs4TN o visite jobs4tn.gov para localizar el AJC más cercano por condado.",
        hours="Varies by local AJC",
        tags="tennessee|employment|american-job-center|jobs4tn|reentry",
        services="Job search assistance|Resume help|Interview coaching|Training referrals|Fair-chance employer connections",
        county="Davidson",
        served_counties=(
            "Bedford|Cannon|Clay|DeKalb|Fentress|Giles|Grundy|Hickman|Humphreys|Lawrence|Lewis|Marshall"
        ),
        coverage="multi",
        _source="https://www.jobs4tn.gov/",
        _source_type="government",
        _confidence="high",
    )

    # Thin-county gap-fill: TDHS Family Assistance for Upper Cumberland and Middle TN counties with legal-aid-only pins
    tn_dhs_thin = [
        ("Cumberland", "Crossville", "1225 South Main Street", "(931) 484-6131"),
        ("Grainger", "Rutledge", "8095 Rutledge Pike", "(865) 828-5247"),
        ("Hancock", "Sneedville", "518 East Main Street", "(423) 733-2531"),
        ("Jackson", "Gainesboro", "109 North Broad Street", "(931) 268-2212"),
        ("Jefferson", "Dandridge", "715 Gay Street", "(865) 397-4024"),
        ("Lincoln", "Fayetteville", "1007 Huntsville Highway", "(931) 433-7800"),
        ("Macon", "Lafayette", "100 Public Square", "(615) 666-2485"),
        ("Maury", "Columbia", "1400 Hatcher Lane", "(931) 380-2567"),
        ("Moore", "Lynchburg", "397 Main Street", "(931) 759-7167"),
        ("Overton", "Livingston", "900 East Broad Street", "(931) 823-7221"),
        ("Perry", "Linden", "113 North Cedar Avenue", "(931) 589-3121"),
        ("Pickett", "Byrdstown", "1000 Pickett Square Drive", "(931) 864-3554"),
        ("Putnam", "Cookeville", "900 South Jefferson Avenue", "(931) 528-1122"),
        ("Roane", "Kingston", "205 West Race Street", "(865) 717-4800"),
        ("Smith", "Carthage", "939 Upper Ferry Road", "(615) 735-0214"),
        ("Trousdale", "Hartsville", "117 Broadway", "(615) 374-3127"),
        ("Van Buren", "Spencer", "1148 Tennessee Avenue", "(931) 946-2442"),
        ("Warren", "McMinnville", "201 Locust Street", "(931) 473-6664"),
        ("Wayne", "Waynesboro", "103 J.V. Mangubat Drive", "(931) 722-5111"),
        ("White", "Sparta", "305 West Bockman Way", "(931) 837-3551"),
    ]
    for county, city, address, phone in tn_dhs_thin:
        if county in existing_fa:
            continue
        add(
            **_dhs_tn(
                county,
                city,
                address,
                phone,
                f"{city} / {county} County",
                _dhs_desc_en(county, city),
                _dhs_desc_es(county, city),
            )
        )
        existing_fa.add(county)

    add(
        name="TDOC Community Supervision — District 52 (Cookeville)",
        category="probation-parole",
        region="Upper Cumberland — Putnam and surrounding counties",
        description=(
            "TDOC District 52 field office in Cookeville supervises probation and parole for Putnam, Cumberland, "
            "Overton, Pickett, White, Van Buren, Jackson, and Fentress County residents including returning citizens "
            "reporting after release from Upper Cumberland jails and state facilities. Officers connect supervisees to "
            "county DHS benefits offices, Jobs4TN workforce centers, and regional food and treatment partners."
        ),
        description_es=(
            "La oficina de campo del Distrito 52 del TDOC en Cookeville supervisa libertad probatoria y condicional "
            "para residentes de los condados Putnam, Cumberland, Overton, Pickett, White, Van Buren, Jackson y "
            "Fentress, incluidos ciudadanos que reportan después de la liberación. Los oficiales conectan a "
            "supervisados con oficinas DHS del condado y centros Jobs4TN."
        ),
        address="900 South Jefferson Avenue, Suite 100",
        city="Cookeville",
        phone="(931) 528-1812",
        email="",
        website="https://www.tn.gov/correction/cs/field-office-directory.html",
        eligibility="Individuals under Tennessee probation or parole supervision in Upper Cumberland counties listed.",
        eligibility_es="Personas bajo supervisión de libertad probatoria o condicional en los condados del Upper Cumberland listados.",
        notes="Co-located near Putnam County DHS Family Assistance; confirm reporting location with assigned officer.",
        notes_es="Ubicado cerca de la oficina DHS del condado Putnam; confirme el sitio de reporte con su oficial asignado.",
        hours="Monday–Friday business hours",
        tags="putnam|upper-cumberland|tennessee|probation|parole|TDOC|reentry",
        services="Probation and parole supervision|Reporting compliance|DHS referrals|Jobs4TN connections|Treatment referrals",
        county="Putnam",
        served_counties="Putnam|Cumberland|Overton|Pickett|White|Van Buren|Jackson|Fentress",
        coverage="multi",
        _source="https://www.tn.gov/correction/cs/field-office-directory.html",
        _source_type="government",
        _confidence="high",
    )
    add(
        name="TDOC Community Supervision — District 51 (Columbia)",
        category="probation-parole",
        region="South-central Middle Tennessee — Maury and surrounding counties",
        description=(
            "TDOC District 51 field office in Columbia supervises probation and parole for Maury, Lincoln, Marshall, "
            "Giles, Lawrence, Wayne, Moore, Perry, and Hickman County residents including returning citizens reporting "
            "after release from south-central Middle Tennessee jails. Officers connect supervisees to county DHS "
            "benefits intake, American Job Centers, and regional reentry partners."
        ),
        description_es=(
            "La oficina de campo del Distrito 51 del TDOC en Columbia supervisa libertad probatoria y condicional "
            "para residentes de los condados Maury, Lincoln, Marshall, Giles, Lawrence, Wayne, Moore, Perry y Hickman. "
            "Los oficiales conectan a supervisados con admisión de beneficios DHS del condado y Centros de Empleo Americanos."
        ),
        address="1223 Trotwood Avenue, Suite 4",
        city="Columbia",
        phone="(931) 380-2568",
        email="",
        website="https://www.tn.gov/correction/cs/field-office-directory.html",
        eligibility="Individuals under Tennessee probation or parole supervision in south-central Middle Tennessee counties listed.",
        eligibility_es="Personas bajo supervisión de libertad probatoria o condicional en los condados del centro-sur de Tennessee listados.",
        notes="Near Legal Aid Society Columbia office and Maury County DHS; contact for reporting requirements only.",
        notes_es="Cerca de la oficina de Legal Aid Society en Columbia y DHS del condado Maury; contacte solo para requisitos de reporte.",
        hours="Monday–Friday business hours",
        tags="maury|middle-tennessee|tennessee|probation|parole|TDOC|reentry",
        services="Probation and parole supervision|Reporting compliance|DHS referrals|Employment connections|Reentry partner referrals",
        county="Maury",
        served_counties="Maury|Lincoln|Marshall|Giles|Lawrence|Wayne|Moore|Perry|Hickman",
        coverage="multi",
        _source="https://www.tn.gov/correction/cs/field-office-directory.html",
        _source_type="government",
        _confidence="high",
    )
    add(
        name="Chattanooga Area Food Bank — Partner Pantry Network",
        category="food-nutrition",
        region="Southeast Tennessee — 8 counties",
        description=(
            "Chattanooga Area Food Bank supplies partner pantries and mobile distributions across southeast Tennessee "
            "counties where legal aid offices provide civil help but local food depth remains thin for returning citizens. "
            "Use the online pantry locator to find the nearest distribution site by ZIP code. Food assistance only—not "
            "housing, employment, or legal services."
        ),
        description_es=(
            "Chattanooga Area Food Bank abastece despensas aliadas y distribuciones móviles en condados del sureste "
            "de Tennessee donde las oficinas de asistencia legal ofrecen ayuda civil pero la profundidad alimentaria "
            "local sigue siendo limitada para ciudadanos que regresan. Use el localizador en línea por código postal."
        ),
        address="2009 Curtain Pole Road",
        city="Chattanooga",
        phone="(423) 622-1800",
        email="",
        website="https://chattfoodbank.org/find-food/",
        eligibility="Open to southeast Tennessee residents needing food assistance through partner agencies.",
        eligibility_es="Abierto a residentes del sureste de Tennessee que necesitan asistencia alimentaria a través de agencias aliadas.",
        notes="Partner pantry hours vary; use chattfoodbank.org locator before visiting.",
        notes_es="Los horarios de despensas aliadas varían; use el localizador de chattfoodbank.org antes de visitar.",
        hours="Office Monday–Friday; partner sites vary",
        tags="southeast-tennessee|food-bank|pantry|reentry",
        services="Food pantry referrals|Mobile food distribution|Partner agency locator|SNAP information",
        county="Hamilton",
        served_counties="Hamilton|Marion|Sequatchie|Bledsoe|Rhea|Meigs|McMinn|Bradley",
        coverage="multi",
        _source="https://chattfoodbank.org/find-food/",
        _source_type="nonprofit",
        _confidence="high",
    )

    from tier_a_anchors import register_tennessee_tier_a_anchors

    register_tennessee_tier_a_anchors(add)
    register_tier_a_tennessee_gaps(add)


def _dcbs_ky(county, city, address, phone, region, desc_en, desc_es):
    return dict(
        name=f"DCBS — {county} County Family Support",
        category="Financial Assistance",
        region=region,
        description=desc_en,
        description_es=desc_es,
        address=address,
        city=city,
        phone=phone,
        email="",
        website="https://kynect.ky.gov/benefits/s/",
        eligibility=f"{county} County residents meeting income and household-size requirements for Medicaid, SNAP, KTAP, and child care assistance; criminal record generally not a barrier.",
        eligibility_es=f"Residentes del condado {county} que cumplan requisitos de ingresos para Medicaid, SNAP, KTAP y cuidado infantil; los antecedentes penales generalmente no son barrera.",
        notes="Apply online at kynect.ky.gov or visit this county DCBS office; bring ID, Social Security card, and release documents if applicable.",
        notes_es="Solicite en kynect.ky.gov o visite esta oficina DCBS del condado; traiga identificación, tarjeta de Seguro Social y documentos de liberación si aplica.",
        hours="Monday–Friday, 8:00 a.m.–4:30 p.m.",
        tags=f"{county.lower()}|kentucky|DCBS|benefits|SNAP|Medicaid|reentry",
        services="Medicaid enrollment|SNAP application|KTAP cash assistance|Child care assistance|kynect benefits navigation",
        county=county,
        served_counties=county,
        coverage="single",
        _source="https://kynect.ky.gov/benefits/s/",
        _source_type="government",
        _confidence="high",
    )


def register_phase3b_kentucky(add, entries=None):
    """County DCBS offices via registry + Tier A depth (probation/parole)."""

    from county_benefits_registry import collect_financial_assistance_counties, register_county_benefits_kentucky

    existing_fa = collect_financial_assistance_counties(entries or [])
    register_county_benefits_kentucky(add, existing_fa)

    add(
        name="Probation & Parole — Maysville (Mason County)",
        category="Probation & Parole",
        region="Maysville / Mason County",
        description=(
            "Kentucky DOC Probation & Parole District 14 field office in Maysville supervises individuals on "
            "felony probation, parole, or conditional discharge in Mason, Bracken, Fleming, Lewis, and Robertson "
            "counties. Officers connect supervisees to DCBS benefits offices, regional workforce centers, and "
            "northeast Kentucky reentry partners. Contact for reporting requirements—not emergency cash or housing."
        ),
        description_es=(
            "La oficina de campo del Distrito 14 de Libertad Condicional y Vigilada del DOC en Maysville supervisa "
            "personas en libertad condicional o vigilada en los condados Mason, Bracken, Fleming, Lewis y Robertson. "
            "Los oficiales conectan a supervisados con oficinas DCBS y aliados de reinserción regional."
        ),
        address="627 E. Main Street",
        city="Maysville",
        phone="(606) 564-5565",
        email="",
        website="https://corrections.ky.gov/Probation-and-Parole/northern/Pages/District-14.aspx",
        eligibility="Individuals under Kentucky probation or parole supervision in District 14 counties.",
        eligibility_es="Personas bajo supervisión de libertad condicional o vigilada del DOC en los condados del Distrito 14.",
        notes="Co-located near Mason County DCBS; call for assigned officer and reporting schedule.",
        notes_es="Ubicado cerca de DCBS del condado Mason; llame para el oficial asignado y horario de reporte.",
        hours="Monday–Friday business hours",
        tags="mason|robertson|northern-kentucky|probation|parole|reentry",
        services="Probation and parole supervision|Reporting compliance|DCBS referrals|Workforce referrals|Reentry partner connections",
        county="Mason",
        served_counties="Mason|Bracken|Fleming|Lewis|Robertson",
        coverage="multi",
        _source="https://corrections.ky.gov/Probation-and-Parole/northern/Pages/District-14.aspx",
        _source_type="government",
        _confidence="high",
    )


def register_tier_a_final_gaps(add):
    """Verified rows for remaining Tier A weak counties after county benefits sync."""
    register_tier_a_tennessee_gaps(add)
    register_tier_a_indiana_gaps(add)


def register_tier_a_tennessee_gaps(add):
    add(
        name="Ascension Saint Thomas Three Rivers Hospital",
        category="healthcare",
        region="Waverly / Humphreys County",
        description=(
            "Ascension Saint Thomas Three Rivers Hospital in Waverly is Humphreys County's critical access hospital "
            "providing emergency, inpatient, outpatient, and specialty care for Tennessee River valley residents "
            "including returning citizens reestablishing medical care after release. The hospital accepts Medicaid, "
            "Medicare, and most insurance; emergency department open 24/7 for acute medical needs."
        ),
        description_es=(
            "Ascension Saint Thomas Three Rivers Hospital en Waverly es el hospital de acceso crítico del condado "
            "Humphreys que ofrece emergencias, hospitalización, ambulatorio y especialidades para residentes del "
            "valle del Tennessee, incluidos ciudadanos que regresan que restablecen atención médica después de la "
            "liberación. Acepta Medicaid, Medicare y la mayoría de seguros; departamento de emergencias 24/7."
        ),
        address="451 Highway 13 South",
        city="Waverly",
        phone="(931) 296-4203",
        email="",
        website="https://healthcare.ascension.org/locations/tennessee/tnnas-three-rivers-hospital-waverly",
        eligibility="Open to Humphreys County and regional residents; Medicaid and Medicare accepted.",
        eligibility_es="Abierto a residentes del condado Humphreys y la región; se acepta Medicaid y Medicare.",
        notes="Primary hospital for Humphreys County; not a substitute for TennCare enrollment—pair with county TDHS office.",
        notes_es="Hospital principal del condado Humphreys; no sustituye la inscripción en TennCare—combine con la oficina TDHS del condado.",
        hours="Emergency department 24/7; outpatient hours vary—call ahead",
        tags="humphreys|tennessee|healthcare|hospital|reentry",
        services="Emergency care|Inpatient services|Outpatient specialty care|Medicaid billing assistance",
        county="Humphreys",
        served_counties="Humphreys",
        coverage="single",
        _source="https://healthcare.ascension.org/-/media/healthcare/compliance-documents/tennessee/2024-chna-ascension-saint-thomas-three-rivers-hospital-humphreys-county.pdf",
        _source_type="government",
        _confidence="high",
    )


def register_tier_a_indiana_gaps(add):
    """Tier A depth rows for Indiana counties still below three core categories after DFR sync."""

    add(
        name="WorkOne — Marion (Grant County)",
        category="employment",
        region="Marion / Grant County",
        description=(
            "WorkOne Marion is the American Job Center serving Grant County and northeast Indiana through Northeast "
            "Indiana Works, connecting justice-involved Hoosiers to career coaching, skills training referrals, "
            "resume development, and second-chance employer networks. Staff assist with unemployment navigation and "
            "Workforce Innovation and Opportunity Act funding for eligible job seekers rebuilding after incarceration."
        ),
        description_es=(
            "WorkOne Marion es el Centro de Empleo Americano que sirve al condado Grant y el noreste de Indiana "
            "a través de Northeast Indiana Works, conectando a hoosiers con antecedentes penales con coaching de "
            "carrera, referencias de capacitación, desarrollo de currículum y redes de empleadores de segunda oportunidad."
        ),
        address="850 North Miller Avenue",
        city="Marion",
        phone="(765) 668-8911",
        email="",
        website="https://www.in.gov/dwd/workone/region-3/",
        eligibility="Indiana residents seeking employment services; justice-involved individuals welcome at WorkOne centers.",
        eligibility_es="Residentes de Indiana que buscan servicios de empleo; personas con antecedentes penales son bienvenidas.",
        notes="Serves Grant County; call ahead to confirm current walk-in hours.",
        notes_es="Sirve al condado Grant; llame con anticipación para confirmar horarios.",
        hours="Monday–Friday, 8:00 a.m.–4:30 p.m.; Thursday opens 10:00 a.m.",
        tags="grant|indiana|employment|WorkOne|reentry",
        services="Career coaching|Job search assistance|Training referrals|Federal bonding information",
        county="Grant",
        served_counties="Grant",
        coverage="single",
        _source="https://neinworks.org/workone-locations/",
        _source_type="government",
        _confidence="high",
    )

    add(
        name="Perry County Memorial Hospital",
        category="healthcare",
        region="Tell City / Perry County",
        description=(
            "Perry County Memorial Hospital in Tell City is the county hospital serving Perry County and south-central "
            "Indiana along the Ohio River, providing emergency, inpatient, and outpatient care for residents including "
            "returning citizens reestablishing primary and specialty medical services after release. Accepts Medicaid, "
            "Medicare, and most commercial insurance."
        ),
        description_es=(
            "Perry County Memorial Hospital en Tell City es el hospital del condado que sirve a Perry County y el "
            "sur de Indiana a lo largo del río Ohio, ofreciendo emergencias, hospitalización y ambulatorio para "
            "residentes, incluidos ciudadanos que regresan que restablecen servicios médicos después de la liberación."
        ),
        address="8885 State Road 237",
        city="Tell City",
        phone="(812) 547-7011",
        email="",
        website="https://www.pchospital.org/",
        eligibility="Open to Perry County residents; Medicaid and Medicare accepted.",
        eligibility_es="Abierto a residentes del condado Perry; se acepta Medicaid y Medicare.",
        notes="County critical access hospital; pair with county DFR for Medicaid enrollment.",
        notes_es="Hospital del condado; combine con DFR del condado para inscripción en Medicaid.",
        hours="Emergency department 24/7; outpatient hours vary",
        tags="perry|indiana|healthcare|hospital|reentry",
        services="Emergency care|Inpatient services|Outpatient care|Medicaid billing assistance",
        county="Perry",
        served_counties="Perry",
        coverage="single",
        _source="https://www.pchospital.org/",
        _source_type="nonprofit",
        _confidence="high",
    )

    add(
        name="WorkOne — Lafayette (Tipton County)",
        category="employment",
        region="Lafayette / Tippecanoe-Tipton",
        description=(
            "WorkOne Lafayette is the West Central Indiana American Job Center serving Tipton County residents through "
            "the Region 4 workforce board, offering career coaching, job search assistance, skills training referrals, "
            "and fair-chance employment connections for justice-involved Hoosiers. Tipton County residents may access "
            "services at this full-service center when the local express office is unavailable."
        ),
        description_es=(
            "WorkOne Lafayette es el Centro de Empleo Americano del centro-oeste de Indiana que sirve a residentes "
            "del condado Tipton a través de la junta de fuerza laboral de la Región 4, ofreciendo coaching de "
            "carrera, búsqueda de empleo y conexiones de empleo justo para hoosiers con antecedentes penales."
        ),
        address="820 Park East Boulevard",
        city="Lafayette",
        phone="(765) 474-5411",
        email="",
        website="https://www.in.gov/dwd/workonewestcentral/locations/",
        eligibility="Indiana residents in Region 4 including Tipton County; justice-involved individuals welcome.",
        eligibility_es="Residentes de Indiana en la Región 4 incluido Tipton; personas con antecedentes penales son bienvenidas.",
        notes="Primary full-service WorkOne for Tipton County per DWD Region 4 guidance.",
        notes_es="WorkOne de servicio completo principal para el condado Tipton según la Región 4 de DWD.",
        hours="Monday–Friday, 8:00 a.m.–4:30 p.m.",
        tags="tipton|indiana|employment|WorkOne|reentry",
        services="Career coaching|Job search assistance|Training referrals|Unemployment navigation",
        county="Tipton",
        served_counties="Tipton",
        coverage="single",
        _source="https://www.in.gov/dwd/workone/region-4/",
        _source_type="government",
        _confidence="high",
    )

    add(
        name="WorkOne Express — Monticello (White County)",
        category="employment",
        region="Monticello / White County",
        description=(
            "WorkOne Express Monticello connects White County job seekers including justice-involved Hoosiers to "
            "Indiana Department of Workforce Development employment services through Community Action Program of "
            "Western Indiana, offering career navigation, job search tools, and referrals to training and supportive "
            "services for residents rebuilding stability after incarceration."
        ),
        description_es=(
            "WorkOne Express Monticello conecta a buscadores de empleo del condado White, incluidos hoosiers con "
            "antecedentes penales, con servicios de empleo del Departamento de Desarrollo Laboral de Indiana a "
            "través de Community Action Program of Western Indiana."
        ),
        address="1500 North Main Street, Suite E",
        city="Monticello",
        phone="(574) 583-6911",
        email="",
        website="https://www.in.gov/dwd/workone/region-4/",
        eligibility="White County Indiana residents seeking employment services.",
        eligibility_es="Residentes del condado White que buscan servicios de empleo.",
        notes="Express office; call ahead for staff availability and appointment options.",
        notes_es="Oficina express; llame con anticipación para disponibilidad del personal.",
        hours="Monday–Friday, 8:00 a.m.–4:30 p.m.; verify before visiting",
        tags="white|indiana|employment|WorkOne|reentry",
        services="Career navigation|Job search assistance|Training referrals|Workforce program intake",
        county="White",
        served_counties="White",
        coverage="single",
        _source="https://www.in.gov/dwd/workone/region-4/",
        _source_type="government",
        _confidence="medium",
    )


def _mdhhs_desc_en(county: str, city: str) -> str:
    return (
        f"The {county} County MDHHS office at {city} is the local benefits intake site for Medicaid, "
        f"Healthy Michigan Plan, SNAP food assistance, cash assistance, and child care subsidies. "
        f"Returning citizens released from {county} County Jail or MDOC custody can apply in person, "
        f"through MI Bridges (newmibridges.michigan.gov), or by calling 1-844-464-3447; staff assist "
        f"with document verification, redetermination deadlines, and emergency food or medical coverage "
        f"when release paperwork is incomplete."
    )


def _mdhhs_desc_es(county: str, city: str) -> str:
    return (
        f"La oficina MDHHS del condado {county} en {city} es el sitio local de admisión de beneficios "
        f"para Medicaid, Plan Saludable de Michigan, SNAP, asistencia en efectivo y subsidios de cuidado "
        f"infantil. Los ciudadanos que regresan liberados de la cárcel del condado {county} o custodia "
        f"del MDOC pueden solicitar en persona, a través de MI Bridges o llamando al 1-844-464-3447; "
        f"el personal ayuda con verificación de documentos y cobertura médica o alimentaria de emergencia."
    )


def _mdhhs_mi(county, city, address, phone, region, desc_en, desc_es):
    return dict(
        name=f"{county} County MDHHS — Family Independence Agency",
        category="financial-assistance",
        region=region,
        description=desc_en,
        description_es=desc_es,
        address=address,
        city=city,
        phone=phone,
        email="",
        website="https://newmibridges.michigan.gov/s/isd-landing-page?language=en_US",
        eligibility=(
            f"{county} County residents meeting income and household-size requirements for Medicaid, "
            f"SNAP, cash assistance, and child care; criminal record generally not a barrier."
        ),
        eligibility_es=(
            f"Residentes del condado {county} que cumplan requisitos de ingresos para Medicaid, SNAP, "
            f"asistencia en efectivo y cuidado infantil; los antecedentes penales generalmente no son barrera."
        ),
        notes=(
            "Apply online at MI Bridges (newmibridges.michigan.gov) or visit the county MDHHS office; "
            "call 1-844-464-3447 for assistance; bring ID and release documents when establishing benefits."
        ),
        notes_es=(
            "Solicite en MI Bridges (newmibridges.michigan.gov) o visite la oficina MDHHS del condado; "
            "llame al 1-844-464-3447; traiga identificación y documentos de liberación."
        ),
        hours="Monday–Friday, 8:00 a.m.–5:00 p.m.",
        tags=f"{county.lower()}|michigan|benefits|SNAP|Medicaid|reentry|MI-Bridges",
        services=(
            "SNAP enrollment|Medicaid and Healthy Michigan Plan|Cash assistance application|"
            "Child care assistance|MI Bridges account support"
        ),
        county=county,
        served_counties=county,
        coverage="single",
        _source="https://mdhhs.michigan.gov/CompositeDirPub/CountyCompositeDirectory.aspx",
        _source_type="government",
        _confidence="high",
    )


def register_phase3b_michigan(add, entries=None):
    """Phase 3b: MDHHS county benefits (registry) + Michigan Works Tier A anchors + thin-county depth."""

    from county_benefits_registry import collect_financial_assistance_counties, register_county_benefits_michigan

    existing_fa = collect_financial_assistance_counties(entries or [])
    register_county_benefits_michigan(add, existing_fa)

    from tier_a_anchors import register_michigan_tier_a_anchors

    register_michigan_tier_a_anchors(add)

    # Regional food bank coverage for thin UP and northeast counties
    add(
        name="Feeding America West Michigan — Partner Pantry Network",
        category="food-nutrition",
        region="West Michigan — 40 counties",
        description=(
            "Feeding America West Michigan distributes food through partner pantries across western and "
            "northern Lower Michigan including many rural counties with thin local reentry directories. "
            "Returning citizens can locate the nearest partner pantry by ZIP code through the online food "
            "finder. Food and nutrition support only—not emergency cash assistance or housing."
        ),
        description_es=(
            "Feeding America West Michigan distribuye alimentos a través de despensas aliadas en el oeste "
            "y norte del Lower Peninsula de Michigan, incluidos condados rurales con pocos recursos locales "
            "de reinserción. Los ciudadanos que regresan pueden localizar la despensa aliada más cercana "
            "por código postal en el buscador en línea."
        ),
        address="864 West River Center Drive NE",
        city="Comstock Park",
        phone="616-784-3250",
        email="",
        website="https://www.feedwm.org/find-food/",
        eligibility="Open to Michigan residents needing food assistance; partner pantry rules vary.",
        eligibility_es="Abierto a residentes de Michigan que necesitan asistencia alimentaria; las reglas varían.",
        notes="Use feedwm.org/find-food for the nearest partner agency by ZIP code.",
        notes_es="Use feedwm.org/find-food para la agencia aliada más cercana por código postal.",
        hours="Office Monday–Friday; partner pantry hours vary",
        tags="west-michigan|food-bank|reentry|pantry|statewide-partner",
        services="Partner pantry referrals|Mobile food distribution|SNAP outreach|Nutrition programs",
        county="Kent",
        served_counties=(
            "Allegan|Antrim|Barry|Benzie|Charlevoix|Clare|Emmet|Grand Traverse|Ionia|Isabella|"
            "Kalkaska|Kent|Lake|Leelanau|Manistee|Mason|Mecosta|Missaukee|Montcalm|Muskegon|"
            "Newaygo|Oceana|Osceola|Ottawa|Wexford"
        ),
        coverage="multi",
        _source="https://www.feedwm.org/find-food/",
        _source_type="nonprofit",
        _confidence="high",
    )


def _fcrc_desc_en(county: str, city: str) -> str:
    return (
        f"{county} County IDHS Family Community Resource Center in {city} is the local benefits intake "
        f"office for SNAP, Medicaid, TANF cash assistance, and child care subsidies for Illinois residents "
        f"including justice-involved individuals reestablishing food and health coverage after release from "
        f"{county} County Jail or IDOC custody. Staff assist with ABE (Application for Benefits Eligibility) "
        f"online applications, document verification, and emergency medical or food coverage when release "
        f"paperwork is incomplete. IDHS accepts SNAP and medical applications from approved IDOC facilities "
        f"within ten days of release through the Pre-Release Program."
    )


def _fcrc_desc_es(county: str, city: str) -> str:
    return (
        f"El Centro de Recursos Comunitarios Familiares IDHS del condado {county} en {city} es la oficina "
        f"local de admisión de beneficios para SNAP, Medicaid, asistencia en efectivo TANF y subsidios de "
        f"cuidado infantil para residentes de Illinois, incluidas personas con antecedentes penales que "
        f"restablecen cobertura alimentaria y de salud después de la liberación. El personal ayuda con "
        f"solicitudes en línea ABE, verificación de documentos y cobertura médica o alimentaria de emergencia. "
        f"IDHS acepta solicitudes SNAP y médicas desde instalaciones IDOC aprobadas dentro de diez días de la liberación."
    )


def _fcrc_il(county, city, address, phone, region, desc_en, desc_es):
    return dict(
        name=f"{county} County IDHS — Family Community Resource Center",
        category="financial-assistance",
        region=region,
        description=desc_en,
        description_es=desc_es,
        address=address,
        city=city,
        phone=phone,
        email="",
        website="https://abe.illinois.gov",
        eligibility=(
            f"{county} County residents meeting income and household-size requirements for Medicaid, SNAP, "
            f"TANF, and child care assistance; criminal record generally not a barrier."
        ),
        eligibility_es=(
            f"Residentes del condado {county} que cumplan requisitos de ingresos para Medicaid, SNAP, TANF "
            f"y cuidado infantil; los antecedentes penales generalmente no son barrera."
        ),
        notes=(
            "Apply online at ABE.Illinois.gov or visit the county FCRC office; call 1-800-843-6154 for "
            "IDHS Help is Here assistance; bring ID and release documents when establishing benefits."
        ),
        notes_es=(
            "Solicite en ABE.Illinois.gov o visite la oficina FCRC del condado; llame al 1-800-843-6154; "
            "traiga identificación y documentos de liberación."
        ),
        hours="Monday–Friday, 8:00 a.m.–5:00 p.m.",
        tags=f"{county.lower()}|illinois|benefits|SNAP|Medicaid|ABE|reentry|FCRC",
        services=(
            "SNAP enrollment|Medicaid application|TANF cash assistance|Child care assistance|"
            "ABE account support|Pre-Release Program coordination"
        ),
        county=county,
        served_counties=county,
        coverage="single",
        _source="https://www.dhs.state.il.us/page.aspx?OfficeType=5&module=12",
        _source_type="government",
        _confidence="high",
    )


def register_phase3b_illinois(add, entries=None):
    """Phase 3b: IDHS FCRC county benefits (registry) + Illinois workNet Tier A anchors."""

    from county_benefits_registry import collect_financial_assistance_counties, register_county_benefits_illinois

    existing_fa = collect_financial_assistance_counties(entries or [])
    register_county_benefits_illinois(add, existing_fa)

    from tier_a_anchors import register_illinois_tier_a_anchors

    register_illinois_tier_a_anchors(add)


def _dohs_desc_en(county: str, city: str) -> str:
    return (
        f"{county} County DoHS field office in {city} is the local benefits intake office for SNAP, "
        f"Medicaid, WV WORKS cash assistance, LIEAP energy help, and child care subsidies for West Virginia "
        f"residents including justice-involved individuals reestablishing food and health coverage after release "
        f"from {county} County Jail or WVDCR custody. Staff assist with WV PATH online applications, document "
        f"verification, and emergency medical or food coverage when release paperwork is incomplete."
    )


def _dohs_desc_es(county: str, city: str) -> str:
    return (
        f"La oficina de campo DoHS del condado {county} en {city} es la oficina local de admisión de beneficios "
        f"para SNAP, Medicaid, asistencia en efectivo WV WORKS, ayuda energética LIEAP y subsidios de cuidado "
        f"infantil para residentes de Virginia Occidental, incluidas personas con antecedentes penales que "
        f"restablecen cobertura alimentaria y de salud después de la liberación. El personal ayuda con "
        f"solicitudes en línea WV PATH, verificación de documentos y cobertura médica o alimentaria de emergencia."
    )


def _dohs_wv(county, city, address, phone, region, desc_en, desc_es):
    return dict(
        name=f"{county} County DoHS — Field Office",
        category="financial-assistance",
        region=region,
        description=desc_en,
        description_es=desc_es,
        address=address,
        city=city,
        phone=phone,
        email="",
        website="https://wvpath.wv.gov",
        eligibility=(
            f"{county} County residents meeting income and household-size requirements for Medicaid, SNAP, "
            f"WV WORKS, and child care assistance; criminal record generally not a barrier."
        ),
        eligibility_es=(
            f"Residentes del condado {county} que cumplan requisitos de ingresos para Medicaid, SNAP, "
            f"WV WORKS y cuidado infantil; los antecedentes penales generalmente no son barrera."
        ),
        notes=(
            "Apply online at wvpath.wv.gov or visit the county DoHS field office; call 1-877-716-1212 for "
            "DoHS Customer Service; bring ID and release documents when establishing benefits."
        ),
        notes_es=(
            "Solicite en wvpath.wv.gov o visite la oficina DoHS del condado; llame al 1-877-716-1212; "
            "traiga identificación y documentos de liberación."
        ),
        hours="Monday–Friday, 8:30 a.m.–5:00 p.m.",
        tags=f"{county.lower()}|west-virginia|benefits|SNAP|Medicaid|WV-PATH|reentry|DoHS",
        services=(
            "SNAP enrollment|Medicaid application|WV WORKS cash assistance|LIEAP energy assistance|"
            "Child care assistance|WV PATH account support"
        ),
        county=county,
        served_counties=county,
        coverage="single",
        _source="https://dhhr.wv.gov/Pages/Field-Offices.aspx",
        _source_type="government",
        _confidence="high",
    )


def register_phase3b_west_virginia(add, entries=None):
    """Phase 3b: DoHS county benefits (registry) + WorkForce WV Tier A anchors."""

    from county_benefits_registry import collect_financial_assistance_counties, register_county_benefits_west_virginia

    existing_fa = collect_financial_assistance_counties(entries or [])
    register_county_benefits_west_virginia(add, existing_fa)

    from tier_a_anchors import register_west_virginia_tier_a_anchors

    register_west_virginia_tier_a_anchors(add)
