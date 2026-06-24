"""Pass 2 gap-fill: category minimums, Tier A regional depth, verified direct-service programs."""


def register_pass2(add):
    """Register verified Michigan programs to meet category minimums and Tier A depth."""

    # --- Tier A regional anchors (UP / northeast / thumb / southwest thin counties) ---
    add(
        name="Alcona Health Center — Federally Qualified Health Center",
        category="healthcare",
        region="Northeast Michigan",
        description=(
            "Federally qualified health center operating medical, dental, behavioral health, and pharmacy "
            "services on a sliding fee scale for residents of rural northeast Michigan including returning "
            "citizens reestablishing primary care after release from Alcona County Jail or MDOC custody. "
            "Multiple clinic sites in Harrisville, Lincoln, and surrounding communities accept Medicaid and "
            "uninsured patients; staff assist with MI Bridges referrals and appointment scheduling."
        ),
        description_es=(
            "Centro de salud calificado federalmente con servicios médicos, dentales, de salud conductual "
            "y farmacia con tarifa escalonada para residentes del noreste rural de Michigan, incluidos "
            "ciudadanos que regresan que restablecen atención primaria después de la liberación. Varios "
            "sitios clínicos aceptan Medicaid y pacientes sin seguro; el personal ayuda con referencias "
            "MI Bridges y programación de citas."
        ),
        address="118 Main Street",
        city="Lincoln",
        phone="989-736-9811",
        email="",
        website="https://www.alconahealthcenters.org",
        eligibility="Open to residents of served northeast Michigan counties; sliding fee based on income; criminal record not a stated barrier.",
        eligibility_es="Abierto a residentes de los condados servidos; tarifa escalonada según ingresos; antecedentes penales no son barrera indicada.",
        notes="Call 989-736-9811 for appointments; Harrisville and Lincoln clinic locations; bring ID and income verification if available.",
        notes_es="Llame al 989-736-9811 para citas; ubicaciones en Harrisville y Lincoln; traiga identificación.",
        hours="Monday–Friday clinic hours; call location for schedule",
        tags="northeast-michigan|FQHC|healthcare|Medicaid|reentry",
        services="Primary care|Behavioral health|Dental services|Pharmacy|Sliding fee scale|Medicaid enrollment assistance",
        county="Alcona",
        served_counties="Alcona|Alpena|Iosco|Montmorency|Ogemaw|Oscoda|Presque Isle",
        coverage="multi",
        _source="https://www.alconahealthcenters.org",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="Northeast Michigan Community Mental Health Services (NeMCMH)",
        category="substance-use-treatment",
        region="Northeast Michigan",
        description=(
            "Prepaid inpatient health plan and community mental health authority providing outpatient "
            "substance use disorder treatment, recovery supports, crisis services, and care coordination "
            "for Medicaid beneficiaries in northeast Michigan including justice-involved individuals "
            "referred by MDOC parole agents, courts, and local hospitals. NeMCMH connects members to "
            "licensed treatment providers and peer recovery coaches across Alpena, Cheboygan, and "
            "surrounding counties."
        ),
        description_es=(
            "Plan de salud prepagado y autoridad de salud mental comunitaria con tratamiento ambulatorio "
            "de trastornos por uso de sustancias, apoyos de recuperación, servicios de crisis y "
            "coordinación de atención para beneficiarios de Medicaid en el noreste de Michigan, incluidas "
            "personas con antecedentes penales referidas por agentes del MDOC y tribunales."
        ),
        address="2785 N. Lincoln Road",
        city="Alpena",
        phone="989-356-2161",
        email="",
        website="https://www.nemcmh.org",
        eligibility="Medicaid beneficiaries and residents accessing publicly funded behavioral health in served counties; intake assessment required.",
        eligibility_es="Beneficiarios de Medicaid y residentes que acceden a salud conductual pública en condados servidos; se requiere evaluación de admisión.",
        notes="Call 989-356-2161 for intake; 24/7 crisis line available; provider network at nemcmh.org.",
        notes_es="Llame al 989-356-2161 para admisión; línea de crisis 24/7; red de proveedores en nemcmh.org.",
        hours="Intake Mon–Fri business hours; crisis services 24/7",
        tags="northeast-michigan|substance-use|mental-health|Medicaid|reentry",
        services="Outpatient SUD treatment|Recovery supports|Crisis services|Care coordination|Peer recovery linkage|Medicaid behavioral health",
        county="Alpena",
        served_counties="Alcona|Alpena|Cheboygan|Iosco|Montmorency|Oscoda|Otsego|Presque Isle",
        coverage="multi",
        _source="https://www.nemcmh.org",
        _source_type="government",
        _confidence="high",
    )
    add(
        name="NEMCSA — Housing & Emergency Services",
        category="housing",
        region="Northeast Michigan",
        description=(
            "Northeast Michigan Community Service Agency providing emergency shelter referrals, "
            "homelessness prevention, rapid rehousing, and utility assistance for low-income residents "
            "across eleven rural counties including returning citizens without stable housing after "
            "release. NEMCSA operates Coordinated Entry intake and connects clients to transitional "
            "housing partners, case management, and MDHHS benefits navigation in Alpena, Roscommon, "
            "and satellite offices."
        ),
        description_es=(
            "Agencia de Servicios Comunitarios del Noreste de Michigan con referencias de refugio de "
            "emergencia, prevención de la falta de vivienda, realojamiento rápido y asistencia con "
            "servicios públicos para residentes de bajos ingresos en once condados rurales, incluidos "
            "ciudadanos que regresan sin vivienda estable. NEMCSA opera admisión de Entrada Coordinada "
            "y conecta con aliados de vivienda transicional y manejo de casos."
        ),
        address="2375 Gordon Road",
        city="Alpena",
        phone="989-356-3474",
        email="",
        website="https://www.nemcsa.org",
        eligibility="Low-income residents of served northeast Michigan counties experiencing housing crisis or utility hardship; intake assessment required.",
        eligibility_es="Residentes de bajos ingresos de condados servidos en crisis de vivienda o dificultades con servicios públicos; se requiere evaluación.",
        notes="Call 989-356-3474 for housing intake; Coordinated Entry required before emergency shelter placement in most counties.",
        notes_es="Llame al 989-356-3474 para admisión de vivienda; Entrada Coordinada requerida antes del refugio de emergencia.",
        hours="Monday–Friday business hours; after-hours housing crisis line varies by county",
        tags="northeast-michigan|housing|emergency-shelter|reentry|utility-assistance",
        services="Emergency shelter referrals|Homelessness prevention|Rapid rehousing|Utility assistance|Coordinated Entry intake|Case management",
        county="Alpena",
        served_counties="Alcona|Alpena|Cheboygan|Crawford|Iosco|Montmorency|Ogemaw|Oscoda|Otsego|Presque Isle|Roscommon",
        coverage="multi",
        _source="https://www.nemcsa.org",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="Legal Services of Northern Michigan",
        category="legal-aid",
        region="Northern Lower Michigan",
        description=(
            "Nonprofit civil legal aid serving low-income residents across 28 northern Michigan counties "
            "with eviction defense, public benefits appeals, family law, and expungement assistance for "
            "returning citizens rebuilding stability. LSNM attorneys represent eligible clients in court "
            "and assist with MI Bridges denials, housing disputes, and civil record matters affecting "
            "employment—not criminal defense."
        ),
        description_es=(
            "Asistencia legal civil sin fines de lucro para residentes de bajos ingresos en 28 condados "
            "del norte de Michigan con defensa de desalojo, apelaciones de beneficios, derecho familiar "
            "y ayuda con eliminación de antecedentes para ciudadanos que regresan. Los abogados de LSNM "
            "representan clientes elegibles en tribunales civiles, no defensa penal."
        ),
        address="800 S. Garfield Avenue",
        city="Traverse City",
        phone="231-941-0661",
        email="",
        website="https://www.lsnm.org",
        eligibility="Low-income residents of served northern Michigan counties with qualifying civil legal problems; income limits apply.",
        eligibility_es="Residentes de bajos ingresos de condados servidos con problemas legales civiles calificados; aplican límites de ingresos.",
        notes="Apply online at lsnm.org or call 231-941-0661; priority for housing and benefits cases affecting reentry stability.",
        notes_es="Solicite en lsnm.org o llame al 231-941-0661; prioridad para casos de vivienda y beneficios que afectan la reinserción.",
        hours="Intake Monday–Friday business hours",
        tags="northern-michigan|legal-aid|housing|expungement|reentry",
        services="Civil legal representation|Eviction defense|Benefits appeals|Family law assistance|Expungement help",
        county="Grand Traverse",
        served_counties=(
            "Alcona|Alpena|Antrim|Benzie|Charlevoix|Cheboygan|Chippewa|Crawford|Emmet|Grand Traverse|"
            "Iosco|Kalkaska|Leelanau|Manistee|Mason|Mecosta|Missaukee|Montmorency|Ogemaw|Oceana|"
            "Oscoda|Otsego|Presque Isle|Roscommon|Wexford"
        ),
        coverage="multi",
        _source="https://www.lsnm.org",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="Food Bank of Eastern Michigan",
        category="food-nutrition",
        region="East Central Michigan",
        description=(
            "Regional food bank distributing to partner pantries, mobile distributions, and school programs "
            "across east-central Michigan including Bay, Saginaw, Tuscola, Huron, Sanilac, and surrounding "
            "counties with thin local reentry directories. Returning citizens locate the nearest partner "
            "pantry by ZIP code through the online food finder; staff can explain pantry hours and ID "
            "requirements. Food assistance only—not cash or housing services."
        ),
        description_es=(
            "Banco de alimentos regional que distribuye a despensas aliadas, distribuciones móviles y "
            "programas escolares en el centro-este de Michigan incluyendo los condados Bay, Saginaw, "
            "Tuscola, Huron y Sanilac. Los ciudadanos que regresan localizan la despensa aliada más "
            "cercana por código postal; solo asistencia alimentaria, no efectivo ni vivienda."
        ),
        address="2300 Lapeer Road",
        city="Flint",
        phone="810-239-7401",
        email="",
        website="https://www.fbem.org",
        eligibility="Open to Michigan residents needing food assistance through partner agencies; pantry rules vary by location.",
        eligibility_es="Abierto a residentes de Michigan que necesitan asistencia alimentaria; las reglas varían según la ubicación.",
        notes="Use fbem.org/find-food for partner pantry locator; call 810-239-7401 for mobile distribution schedules.",
        notes_es="Use fbem.org/find-food para localizar despensas; llame al 810-239-7401 para horarios móviles.",
        hours="Warehouse Mon–Fri; partner pantry hours vary",
        tags="east-central-michigan|food-bank|pantry|reentry",
        services="Partner pantry network|Mobile food distribution|SNAP outreach|School meal partnerships|Online food finder",
        county="Genesee",
        served_counties="Arenac|Bay|Genesee|Gladwin|Gratiot|Huron|Lapeer|Midland|Saginaw|Sanilac|Shiawassee|Tuscola",
        coverage="multi",
        _source="https://www.fbem.org",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="Great Lakes Bay Health Centers",
        category="healthcare",
        region="Great Lakes Bay",
        description=(
            "Federally qualified health center network providing primary care, behavioral health, dental, "
            "and pharmacy services on a sliding fee scale for underserved residents of Bay, Midland, and "
            "Saginaw counties including returning citizens reestablishing medical care after incarceration. "
            "Multiple clinic sites accept Medicaid and uninsured patients; staff coordinate referrals to "
            "specialty care and assist with Healthy Michigan Plan enrollment."
        ),
        description_es=(
            "Red de centros de salud calificados federalmente con atención primaria, salud conductual, "
            "dental y farmacia con tarifa escalonada para residentes desatendidos de los condados Bay, "
            "Midland y Saginaw, incluidos ciudadanos que regresan que restablecen atención médica. "
            "Varios sitios clínicos aceptan Medicaid y pacientes sin seguro."
        ),
        address="1000 Houghton Avenue",
        city="Saginaw",
        phone="989-671-2000",
        email="",
        website="https://www.glbhealth.org",
        eligibility="Open to residents of served counties; sliding fee based on income; criminal record not a stated barrier.",
        eligibility_es="Abierto a residentes de condados servidos; tarifa escalonada según ingresos; antecedentes penales no son barrera indicada.",
        notes="Call 989-671-2000 for appointments; locations in Saginaw, Bay City, and Midland; bring ID and proof of income.",
        notes_es="Llame al 989-671-2000 para citas; ubicaciones en Saginaw, Bay City y Midland; traiga identificación.",
        hours="Monday–Friday clinic hours; contact location for schedule",
        tags="great-lakes-bay|FQHC|healthcare|Medicaid|reentry",
        services="Primary care|Behavioral health|Dental services|Pharmacy|Sliding fee scale|Medicaid enrollment assistance",
        county="Saginaw",
        served_counties="Bay|Midland|Saginaw|Arenac",
        coverage="multi",
        _source="https://www.glbhealth.org",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="Legal Services of Central Michigan",
        category="legal-aid",
        region="Central Michigan",
        description=(
            "Nonprofit civil legal aid serving low-income residents in central Michigan including Gratiot, "
            "Gladwin, Arenac, and Midland counties with housing, public benefits, family law, and consumer "
            "matters affecting reentry stability. LSSCM attorneys provide eviction defense and benefits "
            "appeals for eligible clients; does not handle criminal defense. Intake through centralized "
            "phone line and online application."
        ),
        description_es=(
            "Asistencia legal civil sin fines de lucro para residentes de bajos ingresos en el centro de "
            "Michigan incluyendo los condados Gratiot, Gladwin, Arenac y Midland con vivienda, beneficios "
            "públicos y asuntos de consumo que afectan la estabilidad en reinserción. No maneja defensa penal."
        ),
        address="300 N. Washington Square, Suite 100",
        city="Lansing",
        phone="888-783-8190",
        email="",
        website="https://www.lsscm.org",
        eligibility="Low-income residents of served central Michigan counties with qualifying civil legal problems.",
        eligibility_es="Residentes de bajos ingresos de condados servidos con problemas legales civiles calificados.",
        notes="Call 888-783-8190 or apply at lsscm.org; satellite offices in Mount Pleasant and Saginaw.",
        notes_es="Llame al 888-783-8190 o solicite en lsscm.org; oficinas satélite en Mount Pleasant y Saginaw.",
        hours="Intake Monday–Friday business hours",
        tags="central-michigan|legal-aid|housing|benefits|reentry",
        services="Civil legal representation|Eviction defense|Benefits advocacy|Family law assistance|Consumer legal help",
        county="Ingham",
        served_counties="Arenac|Gladwin|Gratiot|Midland|Bay|Saginaw|Isabella|Clare",
        coverage="multi",
        _source="https://www.lsscm.org",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="Summit Pointe — Behavioral Health & Substance Use Treatment",
        category="substance-use-treatment",
        region="Southwest Michigan",
        description=(
            "Community mental health and substance use treatment provider serving Calhoun, Branch, and "
            "Barry counties with outpatient counseling, medication-assisted treatment, crisis services, "
            "and recovery supports for Medicaid beneficiaries including justice-involved individuals "
            "referred by MDOC, courts, and local hospitals. Summit Pointe coordinates with Kinexus "
            "Offender Success partners for reentry care continuity."
        ),
        description_es=(
            "Proveedor de salud mental comunitaria y tratamiento de sustancias que sirve a los condados "
            "Calhoun, Branch y Barry con consejería ambulatoria, tratamiento asistido con medicamentos, "
            "servicios de crisis y apoyos de recuperación para beneficiarios de Medicaid, incluidas "
            "personas con antecedentes penales referidas por MDOC y tribunales."
        ),
        address="140 West Michigan Avenue",
        city="Battle Creek",
        phone="269-966-1460",
        email="",
        website="https://www.summitpointe.org",
        eligibility="Medicaid beneficiaries and residents accessing publicly funded behavioral health in served counties; intake required.",
        eligibility_es="Beneficiarios de Medicaid y residentes que acceden a salud conductual pública; se requiere admisión.",
        notes="Call 269-966-1460 for intake; 24/7 crisis line; multiple outpatient sites in Battle Creek and Albion.",
        notes_es="Llame al 269-966-1460 para admisión; línea de crisis 24/7; sitios ambulatorios en Battle Creek y Albion.",
        hours="Intake Mon–Fri business hours; crisis services 24/7",
        tags="southwest-michigan|substance-use|mental-health|Medicaid|reentry",
        services="Outpatient SUD treatment|Medication-assisted treatment|Crisis services|Recovery supports|Care coordination",
        county="Calhoun",
        served_counties="Calhoun|Branch|Barry",
        coverage="multi",
        _source="https://www.summitpointe.org",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="Legal Aid of Western Michigan",
        category="legal-aid",
        region="West Michigan",
        description=(
            "Nonprofit civil legal aid serving low-income residents across 17 west and southwest Michigan "
            "counties including Branch, Calhoun, and St. Joseph with eviction defense, public benefits "
            "appeals, family law, and expungement assistance for returning citizens. LAWM attorneys "
            "represent eligible clients in court; does not provide criminal defense representation."
        ),
        description_es=(
            "Asistencia legal civil sin fines de lucro para residentes de bajos ingresos en 17 condados "
            "del oeste y suroeste de Michigan incluyendo Branch, Calhoun y St. Joseph con defensa de "
            "desalojo, apelaciones de beneficios y ayuda con eliminación de antecedentes."
        ),
        address="1104 S. Westnedge Avenue",
        city="Kalamazoo",
        phone="888-783-8190",
        email="",
        website="https://www.lawestmichigan.org",
        eligibility="Low-income residents of served west Michigan counties with qualifying civil legal problems.",
        eligibility_es="Residentes de bajos ingresos de condados servidos con problemas legales civiles calificados.",
        notes="Apply at lawestmichigan.org or call 888-783-8190; offices in Kalamazoo, Grand Rapids, and Benton Harbor.",
        notes_es="Solicite en lawestmichigan.org o llame al 888-783-8190; oficinas en Kalamazoo, Grand Rapids y Benton Harbor.",
        hours="Intake Monday–Friday business hours",
        tags="west-michigan|legal-aid|housing|expungement|reentry",
        services="Civil legal representation|Eviction defense|Benefits advocacy|Family law assistance|Expungement help",
        county="Kalamazoo",
        served_counties="Branch|Calhoun|St. Joseph|Berrien|Cass|Van Buren|Kalamazoo|Allegan|Barry|Ionia|Kent|Lake|Mason|Mecosta|Montcalm|Muskegon|Ottawa",
        coverage="multi",
        _source="https://www.lawestmichigan.org",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="Community Action Agency of South Central Michigan",
        category="basic-needs",
        region="Southwest Michigan",
        description=(
            "Community Action Agency providing emergency utility assistance, weatherization, food "
            "distribution, and case management for low-income residents of Calhoun and Branch counties "
            "including returning citizens rebuilding stability after incarceration. CAASCM operates "
            "Battle Creek and Coldwater service centers with walk-in intake for eligible households "
            "facing shutoff notices or food insecurity."
        ),
        description_es=(
            "Agencia de Acción Comunitaria con asistencia de emergencia para servicios públicos, "
            "climatización, distribución de alimentos y manejo de casos para residentes de bajos ingresos "
            "de los condados Calhoun y Branch, incluidos ciudadanos que regresan. CAASCM opera centros "
            "de servicio en Battle Creek y Coldwater con admisión sin cita para hogares elegibles."
        ),
        address="175 Main Street",
        city="Battle Creek",
        phone="269-965-7766",
        email="",
        website="https://www.caascm.org",
        eligibility="Low-income residents of Calhoun and Branch counties; income documentation required for utility and weatherization programs.",
        eligibility_es="Residentes de bajos ingresos de Calhoun y Branch; se requiere documentación de ingresos para programas de servicios públicos.",
        notes="Call 269-965-7766 for intake; utility assistance requires shutoff notice or past-due bill; food pantry hours vary.",
        notes_es="Llame al 269-965-7766 para admisión; asistencia de servicios públicos requiere aviso de corte; horarios de despensa varían.",
        hours="Monday–Friday business hours; food pantry hours vary",
        tags="southwest-michigan|basic-needs|utility-assistance|food|reentry",
        services="Emergency utility assistance|Weatherization|Food distribution|Case management|Emergency aid",
        county="Calhoun",
        served_counties="Calhoun|Branch",
        coverage="multi",
        _source="https://www.caascm.org",
        _source_type="nonprofit",
        _confidence="high",
    )

    # --- family-children (3) ---
    add(
        name="CAN Council Great Lakes Bay — Parent Education & Family Support",
        category="family-children",
        region="Great Lakes Bay",
        description=(
            "Child abuse prevention and family support nonprofit serving Bay, Saginaw, and surrounding "
            "counties with parenting education, home visiting, and family reunification support for "
            "parents rebuilding relationships with children after incarceration or CPS involvement. "
            "CAN Council offers evidence-based Nurturing Parenting classes, supervised visitation "
            "coordination referrals, and case management connecting families to housing and treatment partners."
        ),
        description_es=(
            "Organización de prevención del abuso infantil y apoyo familiar que sirve a los condados Bay, "
            "Saginaw y circundantes con educación para padres, visitas domiciliarias y apoyo de reunificación "
            "familiar para padres que reconstruyen relaciones con hijos después de la encarcelación o "
            "involucramiento con CPS. Ofrece clases Nurturing Parenting y referencias de manejo de casos."
        ),
        address="1311 N. Michigan Avenue",
        city="Saginaw",
        phone="989-752-7226",
        email="",
        website="https://www.cancouncil.org",
        eligibility="Parents and caregivers in served counties seeking parenting support or reunification services; referral from CPS or self-referral accepted for some programs.",
        eligibility_es="Padres y cuidadores en condados servidos que buscan apoyo de crianza o servicios de reunificación; referencia de CPS o autorreferencia aceptada.",
        notes="Call 989-752-7226 for program enrollment; parenting classes offered in Saginaw and Bay City; not an emergency shelter.",
        notes_es="Llame al 989-752-7226 para inscripción; clases para padres en Saginaw y Bay City; no es refugio de emergencia.",
        hours="Monday–Friday business hours; class schedules vary",
        tags="saginaw|bay|family-children|parenting|reunification|reentry",
        services="Parenting education|Home visiting|Family reunification support|Nurturing Parenting classes|Case management referrals",
        county="Saginaw",
        served_counties="Saginaw|Bay|Midland",
        coverage="multi",
        _source="https://www.cancouncil.org",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="Detroit Parent Network — Family Support Services",
        category="family-children",
        region="Detroit / Wayne County",
        description=(
            "Wayne County nonprofit strengthening families through parenting workshops, fatherhood "
            "engagement programs, and resource navigation for parents returning from incarceration "
            "seeking reunification with children. Detroit Parent Network connects participants to "
            "child care subsidies, MI Bridges benefits, housing partners, and court-approved parenting "
            "classes required for custody restoration."
        ),
        description_es=(
            "Organización sin fines de lucro del condado Wayne que fortalece familias mediante talleres "
            "de crianza, programas de involucramiento de la paternidad y navegación de recursos para "
            "padres que regresan de la encarcelación buscando reunificación con hijos. Conecta a "
            "participantes con subsidios de cuidado infantil, beneficios MI Bridges y clases de crianza."
        ),
        address="726 Lothrop Road",
        city="Detroit",
        phone="313-309-8400",
        email="",
        website="https://www.detroitparentnetwork.org",
        eligibility="Wayne County parents and caregivers; programs serve justice-involved parents seeking family reunification support.",
        eligibility_es="Padres y cuidadores del condado Wayne; programas sirven a padres con antecedentes penales que buscan reunificación familiar.",
        notes="Call 313-309-8400 for enrollment; fatherhood and parenting workshops offered weekly; connects to MDHHS and local courts.",
        notes_es="Llame al 313-309-8400 para inscripción; talleres semanales; conecta con MDHHS y tribunales locales.",
        hours="Monday–Friday business hours; workshop times vary",
        tags="detroit|wayne|family-children|parenting|fatherhood|reentry",
        services="Parenting workshops|Fatherhood engagement|Family reunification navigation|Child care resource referrals|Court-approved parenting classes",
        county="Wayne",
        served_counties="Wayne",
        coverage="single",
        _source="https://www.detroitparentnetwork.org",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="Southwest Counseling Solutions — Family Reunification Program",
        category="family-children",
        region="Detroit / Wayne County",
        description=(
            "Detroit behavioral health agency offering family reunification therapy, parenting support, "
            "and home-based services for parents with substance use or mental health needs working to "
            "regain custody of children after incarceration or CPS involvement. Southwest Counseling "
            "Solutions accepts Medicaid and coordinates with Wayne County courts, MDHHS, and MDOC "
            "Offender Success partners for integrated family recovery planning."
        ),
        description_es=(
            "Agencia de salud conductual de Detroit con terapia de reunificación familiar, apoyo de "
            "crianza y servicios basados en el hogar para padres con necesidades de salud mental o uso "
            "de sustancias que trabajan para recuperar la custodia de hijos después de la encarcelación. "
            "Acepta Medicaid y coordina con tribunales del condado Wayne y aliados Offender Success."
        ),
        address="1700 St. Antoine Street",
        city="Detroit",
        phone="313-963-6601",
        email="",
        website="https://www.southwestcounseling.com",
        eligibility="Wayne County parents with behavioral health needs seeking family reunification; Medicaid accepted; court or CPS referral may be required.",
        eligibility_es="Padres del condado Wayne con necesidades de salud conductual que buscan reunificación; acepta Medicaid; puede requerir referencia judicial o de CPS.",
        notes="Call 313-963-6601 for intake assessment; home-based services available; coordinates with DWIHN provider network.",
        notes_es="Llame al 313-963-6601 para evaluación; servicios en el hogar disponibles; coordina con red DWIHN.",
        hours="Intake Mon–Fri business hours; home visits by appointment",
        tags="detroit|wayne|family-children|reunification|behavioral-health|reentry",
        services="Family reunification therapy|Parenting support|Home-based services|Medicaid behavioral health|Court coordination",
        county="Wayne",
        served_counties="Wayne",
        coverage="single",
        _source="https://www.southwestcounseling.com",
        _source_type="nonprofit",
        _confidence="high",
    )

    # --- peer-support (3 more; 1 exists) ---
    add(
        name="Detroit Recovery Project — Peer Recovery Coaching",
        category="peer-support",
        region="Detroit / Wayne County",
        description=(
            "Recovery Community Organization providing certified peer recovery coaches, recovery groups, "
            "and reentry navigation for justice-involved Wayne County residents maintaining sobriety after "
            "release. Detroit Recovery Project peers offer mentoring, transportation to treatment "
            "appointments, and connections to housing and employment partners—non-clinical support "
            "complementing DWIHN and MDOC Offender Success services."
        ),
        description_es=(
            "Organización Comunitaria de Recuperación con coaches de recuperación certificados, grupos de "
            "recuperación y navegación de reinserción para residentes del condado Wayne con antecedentes "
            "penales que mantienen sobriedad después de la liberación. Los pares ofrecen mentoría y "
            "conexiones a aliados de vivienda y empleo—apoyo no clínico complementario a DWIHN y MDOC."
        ),
        address="1121 East McNichols Road",
        city="Detroit",
        phone="313-331-6053",
        email="",
        website="https://www.detroitrecoveryproject.org",
        eligibility="Wayne County residents in recovery from substance use; justice-involved individuals welcome; no insurance required for peer services.",
        eligibility_es="Residentes del condado Wayne en recuperación de sustancias; personas con antecedentes penales bienvenidas; no se requiere seguro para servicios entre pares.",
        notes="Call 313-331-6053 for peer coach assignment; walk-in recovery groups at McNichols location; complements clinical treatment.",
        notes_es="Llame al 313-331-6053 para asignación de coach; grupos de recuperación sin cita; complementa tratamiento clínico.",
        hours="Peer services Mon–Sat; group schedules vary",
        tags="detroit|wayne|peer-support|recovery|reentry",
        services="Peer recovery coaching|Recovery support groups|Reentry navigation|Treatment appointment support|Housing and employment linkages",
        county="Wayne",
        served_counties="Wayne",
        coverage="single",
        _source="https://www.detroitrecoveryproject.org",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="West Michigan Recovery Community Organization (WMRCO)",
        category="peer-support",
        region="Grand Rapids / Kent County",
        description=(
            "Certified Recovery Community Organization connecting Kent and surrounding west Michigan "
            "counties to peer recovery coaches, mutual aid groups, and recovery community events for "
            "individuals maintaining sobriety after incarceration or treatment. WMRCO peers with lived "
            "experience provide mentoring, wellness planning, and warm referrals to Michigan Works! "
            "and Hope Network reentry partners."
        ),
        description_es=(
            "Organización Comunitaria de Recuperación certificada que conecta al condado Kent y el oeste "
            "de Michigan con coaches de recuperación, grupos de ayuda mutua y eventos comunitarios de "
            "recuperación para personas que mantienen sobriedad después de la encarcelación o tratamiento."
        ),
        address="678 Front Avenue NW, Suite 150",
        city="Grand Rapids",
        phone="616-356-1276",
        email="",
        website="https://www.wmrco.org",
        eligibility="Individuals in recovery seeking peer support in west Michigan; justice-involved residents welcome.",
        eligibility_es="Personas en recuperación que buscan apoyo entre pares en el oeste de Michigan; residentes con antecedentes penales bienvenidos.",
        notes="Call 616-356-1276 for peer coach matching; recovery community center hours posted at wmrco.org.",
        notes_es="Llame al 616-356-1276 para emparejamiento con coach; horarios del centro en wmrco.org.",
        hours="Recovery center Mon–Sat; call for current schedule",
        tags="grand-rapids|kent|peer-support|recovery|reentry",
        services="Peer recovery coaching|Mutual aid groups|Recovery community events|Wellness planning|Reentry warm referrals",
        county="Kent",
        served_counties="Kent|Barry|Ionia|Montcalm",
        coverage="multi",
        _source="https://www.wmrco.org",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="Face Addiction Now (FAN) — Michigan Chapter Peer Support",
        category="peer-support",
        region="Southeast Michigan",
        description=(
            "Statewide family and peer support network connecting Michigan residents affected by "
            "addiction to certified peer recovery coaches, family education, and naloxone training. "
            "FAN Michigan chapters in metro Detroit and Lansing serve justice-involved individuals "
            "and families navigating reentry alongside a loved one in recovery, offering non-clinical "
            "mentoring and linkage to treatment through MDHHS Recovery Help Line partners."
        ),
        description_es=(
            "Red estatal de apoyo familiar y entre pares que conecta a residentes de Michigan afectados "
            "por adicciones con coaches de recuperación certificados, educación familiar y capacitación "
            "en naloxona. Los capítulos FAN en el metro de Detroit y Lansing sirven a personas con "
            "antecedentes penales y familias navegando la reinserción junto a un ser querido en recuperación."
        ),
        address="",
        city="Lansing",
        phone="517-999-3646",
        email="",
        website="https://faceaddictionnow.org/michigan/",
        eligibility="Open to individuals and families affected by addiction in Michigan; peer services free; no criminal-record restrictions.",
        eligibility_es="Abierto a personas y familias afectadas por adicciones en Michigan; servicios entre pares gratuitos; sin restricciones de antecedentes.",
        notes="Visit faceaddictionnow.org/michigan for chapter contacts; naloxone training events listed online; complements clinical treatment.",
        notes_es="Visite faceaddictionnow.org/michigan para contactos de capítulos; eventos de capacitación en naloxona en línea.",
        hours="Chapter hours vary; online resources 24/7",
        tags="statewide|peer-support|recovery|family|reentry",
        services="Peer recovery coaching|Family education|Naloxone training|Recovery community connections|Treatment linkage",
        county="Ingham",
        served_counties="Wayne|Oakland|Macomb|Washtenaw|Ingham",
        coverage="multi",
        _source="https://faceaddictionnow.org/michigan/",
        _source_type="nonprofit",
        _confidence="high",
    )

    # --- id-documentation (2 more) ---
    add(
        name="Michigan Vital Records — Birth Certificate Requests",
        category="id-documentation",
        region="Statewide",
        description=(
            "Official Michigan Department of Health and Human Services vital records service for "
            "ordering certified birth certificates needed to obtain state ID, driver's licenses, "
            "and MI Bridges benefits after incarceration. Returning citizens can apply online, by "
            "mail, or in person at the Lansing office; MDOC reentry staff and legal aid partners "
            "often assist with gathering identity documents required for SOS branch visits."
        ),
        description_es=(
            "Servicio oficial de registros vitales del Departamento de Salud y Servicios Humanos de "
            "Michigan para solicitar certificados de nacimiento certificados necesarios para obtener "
            "identificación estatal, licencias de conducir y beneficios MI Bridges después de la "
            "encarcelación. Los ciudadanos que regresan pueden solicitar en línea, por correo o en persona."
        ),
        address="333 S. Grand Avenue",
        city="Lansing",
        phone="517-335-8666",
        email="",
        website="https://www.michigan.gov/mdhhs/0,5882,7-339-71551_4645---,00.html",
        eligibility="Individuals who can provide required identity information to request their own or eligible family member's birth certificate; fees apply.",
        eligibility_es="Personas que puedan proporcionar información de identidad requerida para solicitar certificado de nacimiento propio o de familiar elegible; aplican tarifas.",
        notes="Order online at Michigan.gov vital records portal; processing times vary; needed before SOS ID issuance.",
        notes_es="Solicite en línea en el portal de registros vitales de Michigan.gov; tiempos de procesamiento varían.",
        hours="Online 24/7; Lansing office Mon–Fri business hours",
        tags="statewide|id-documentation|birth-certificate|vital-records|reentry",
        services="Birth certificate issuance|Vital records requests|Online ordering|Identity document support",
        county="Ingham",
        served_counties="",
        coverage="statewide",
        _source="https://www.michigan.gov/mdhhs/0,5882,7-339-71551_4645---,00.html",
        _source_type="government",
        _confidence="high",
    )
    add(
        name="Street Democracy — ID & Vital Records Clinic",
        category="id-documentation",
        region="Detroit / Wayne County",
        description=(
            "Detroit nonprofit legal clinic helping unhoused and justice-involved Wayne County residents "
            "obtain Michigan state identification, birth certificates, and Social Security cards needed "
            "for employment and MI Bridges enrollment. Street Democracy attorneys and volunteers assist "
            "with fee waivers, SOS appointment scheduling, and document gathering for returning citizens "
            "without stable address or release paperwork."
        ),
        description_es=(
            "Clínica legal sin fines de lucro de Detroit que ayuda a residentes sin hogar y con "
            "antecedentes penales del condado Wayne a obtener identificación estatal de Michigan, "
            "certificados de nacimiento y tarjetas de Seguro Social necesarios para empleo e inscripción "
            "en MI Bridges. Abogados y voluntarios ayudan con exenciones de tarifas y reunión de documentos."
        ),
        address="7655 Outer Drive East",
        city="Detroit",
        phone="313-922-0910",
        email="",
        website="https://www.streetdemocracy.org",
        eligibility="Wayne County residents experiencing homelessness or recent release from incarceration lacking ID documents; intake required.",
        eligibility_es="Residentes del condado Wayne sin hogar o recién liberados de la encarcelación sin documentos de identificación; se requiere admisión.",
        notes="Call 313-922-0910 for clinic appointment; bring any available release papers; partners with SOS and MDHHS offices.",
        notes_es="Llame al 313-922-0910 para cita de clínica; traiga documentos de liberación disponibles.",
        hours="Clinic days by appointment; call for schedule",
        tags="detroit|wayne|id-documentation|homeless|reentry",
        services="State ID assistance|Birth certificate help|Social Security card support|Fee waiver assistance|SOS appointment scheduling",
        county="Wayne",
        served_counties="Wayne",
        coverage="single",
        _source="https://www.streetdemocracy.org",
        _source_type="nonprofit",
        _confidence="high",
    )

    # --- basic-needs (8 more; 2 exist) ---
    _basic_needs_rows = [
        dict(
            name="Capuchin Soup Kitchen — Services Center",
            region="Detroit / Wayne County",
            city="Detroit", county="Wayne", served="Wayne",
            phone="313-579-2100", website="https://www.cskdetroit.org",
            address="1264 Meldrum Street",
            desc_en=(
                "Detroit soup kitchen and services center providing hot meals, clothing, hygiene kits, "
                "and shower facilities for unhoused and low-income Wayne County residents including "
                "returning citizens without stable housing after release. Capuchin Services Center "
                "operates weekday meal service and connects guests to housing navigation and MDHHS "
                "benefits partners on-site."
            ),
            desc_es=(
                "Comedor y centro de servicios de Detroit con comidas calientes, ropa, kits de higiene "
                "e instalaciones de ducha para residentes sin hogar y de bajos ingresos del condado Wayne, "
                "incluidos ciudadanos que regresan sin vivienda estable. Opera servicio de comidas entre "
                "semana y conecta con aliados de vivienda y beneficios MDHHS."
            ),
        ),
        dict(
            name="EightCAP, Inc. — Community Action Agency",
            region="Central Michigan",
            city="Greenville", county="Montcalm", served="Gratiot|Montcalm|Isabella",
            phone="989-754-3440", website="https://www.eightcap.org",
            address="604 S. Lincoln Avenue",
            desc_en=(
                "Community Action Agency serving Gratiot, Montcalm, and Isabella counties with emergency "
                "utility assistance, food distribution, weatherization, and case management for low-income "
                "residents including returning citizens in rural central Michigan. EightCAP operates "
                "service centers in Greenville and Mount Pleasant with walk-in intake for eligible households."
            ),
            desc_es=(
                "Agencia de Acción Comunitaria que sirve a los condados Gratiot, Montcalm e Isabella con "
                "asistencia de emergencia para servicios públicos, distribución de alimentos, climatización "
                "y manejo de casos para residentes de bajos ingresos, incluidos ciudadanos que regresan "
                "en el centro rural de Michigan."
            ),
        ),
        dict(
            name="Mid Michigan Community Action Agency",
            region="Mid Michigan",
            city="Farwell", county="Clare", served="Clare|Gladwin|Arenac|Osceola",
            phone="989-386-3800", website="https://www.midmichigancaa.org",
            address="4522 Winfield Road",
            desc_en=(
                "Community Action Agency providing emergency aid, utility assistance, food pantry access, "
                "and weatherization for low-income residents of Clare, Gladwin, Arenac, and Osceola counties "
                "including justice-involved individuals rebuilding stability after release from local jails "
                "or MDOC custody. Mid Michigan CAA operates service centers with income-based eligibility."
            ),
            desc_es=(
                "Agencia de Acción Comunitaria con ayuda de emergencia, asistencia de servicios públicos, "
                "acceso a despensa de alimentos y climatización para residentes de bajos ingresos de "
                "Clare, Gladwin, Arenac y Osceola, incluidas personas con antecedentes penales."
            ),
        ),
        dict(
            name="The Salvation Army — Western Michigan & Northern Indiana Division",
            region="West Michigan",
            city="Grand Rapids", county="Kent", served="Kent|Ottawa|Muskegon|Allegan",
            phone="616-459-3433", website="https://centralusa.salvationarmy.org/wmni",
            address="1215 East Fulton Street",
            desc_en=(
                "Regional Salvation Army division providing emergency shelter, food assistance, utility "
                "aid, and clothing for west Michigan residents including returning citizens in Kent, "
                "Ottawa, and Muskegon counties. Corps community centers offer meals, case management "
                "referrals, and seasonal assistance programs with walk-in intake at Grand Rapids headquarters."
            ),
            desc_es=(
                "División regional de Salvation Army con refugio de emergencia, asistencia alimentaria, "
                "ayuda con servicios públicos y ropa para residentes del oeste de Michigan, incluidos "
                "ciudadanos que regresan en los condados Kent, Ottawa y Muskegon."
            ),
        ),
        dict(
            name="Goodwill Industries of West Michigan — Clothing & Essentials",
            region="Grand Rapids / Kent County",
            city="Grand Rapids", county="Kent", served="Kent|Ottawa|Allegan",
            phone="616-532-4200", website="https://www.goodwillwm.org",
            address="455 Grand Avenue NE",
            desc_en=(
                "Goodwill retail and community services providing low-cost clothing, household essentials, "
                "and voucher programs for justice-involved Kent County residents establishing stability "
                "after release. Goodwill West Michigan partners with Michigan Works! and local reentry "
                "programs to distribute interview clothing and basic necessities through referral."
            ),
            desc_es=(
                "Goodwill con ropa de bajo costo, artículos esenciales para el hogar y programas de "
                "vouchers para residentes del condado Kent con antecedentes penales que establecen "
                "estabilidad después de la liberación. Se asocia con Michigan Works! para ropa de entrevistas."
            ),
        ),
        dict(
            name="NEMCSA — Basic Needs & Emergency Assistance",
            category_override="basic-needs",
            region="Northeast Michigan",
            city="Alpena", county="Alpena",
            served="Alcona|Alpena|Cheboygan|Crawford|Iosco|Montmorency|Ogemaw|Oscoda|Otsego|Presque Isle|Roscommon",
            phone="989-356-3474", website="https://www.nemcsa.org",
            address="2375 Gordon Road",
            desc_en=(
                "Northeast Michigan Community Service Agency emergency assistance program providing utility "
                "aid, food boxes, clothing vouchers, and transportation assistance for low-income residents "
                "across eleven rural counties including returning citizens without resources after release. "
                "Separate from NEMCSA housing programs; walk-in intake at Alpena headquarters."
            ),
            desc_es=(
                "Programa de asistencia de emergencia de NEMCSA con ayuda de servicios públicos, cajas de "
                "alimentos, vouchers de ropa y asistencia de transporte para residentes de bajos ingresos "
                "en once condados rurales, incluidos ciudadanos que regresan sin recursos."
            ),
        ),
        dict(
            name="Macomb County Community Services — Emergency Assistance",
            region="Macomb County",
            city="Mount Clemens", county="Macomb", served="Macomb",
            phone="586-469-6999", website="https://www.macombgov.org/departments/community-services",
            address="21885 Dunham Road",
            desc_en=(
                "Macomb County government community services department providing emergency utility assistance, "
                "food referrals, and basic needs navigation for low-income county residents including "
                "returning citizens reestablishing household stability after incarceration. Staff connect "
                "eligible households to MDHHS benefits, local pantries, and Salvation Army partners."
            ),
            desc_es=(
                "Departamento de servicios comunitarios del condado Macomb con asistencia de emergencia "
                "para servicios públicos, referencias de alimentos y navegación de necesidades básicas "
                "para residentes de bajos ingresos, incluidos ciudadanos que regresan."
            ),
        ),
        dict(
            name="Ozone House — Basic Needs for Youth",
            region="Ann Arbor / Washtenaw County",
            city="Ann Arbor", county="Washtenaw", served="Washtenaw",
            phone="734-662-2222", website="https://www.ozonehouse.org",
            address="1705 Washtenaw Avenue",
            desc_en=(
                "Washtenaw County youth services agency providing clothing, hygiene supplies, meals, and "
                "crisis shelter for young adults ages 18–24 including those aging out of foster care or "
                "returning from juvenile or adult incarceration without family support. Ozone House "
                "Drop-In Center offers walk-in basic needs assistance and case management referrals."
            ),
            desc_es=(
                "Agencia de servicios para jóvenes del condado Washtenaw con ropa, artículos de higiene, "
                "comidas y refugio de crisis para adultos jóvenes de 18 a 24 años, incluidos quienes "
                "regresan de la encarcelación juvenil o adulta sin apoyo familiar."
            ),
        ),
    ]
    for row in _basic_needs_rows:
        add(
            name=row["name"],
            category=row.get("category_override", "basic-needs"),
            region=row["region"],
            description=row["desc_en"],
            description_es=row["desc_es"],
            address=row["address"],
            city=row["city"],
            phone=row["phone"],
            email="",
            website=row["website"],
            eligibility=f"Low-income residents of served counties; income documentation may be required; justice-involved individuals generally eligible for emergency programs.",
            eligibility_es="Residentes de bajos ingresos de condados servidos; puede requerir documentación de ingresos; personas con antecedentes penales generalmente elegibles.",
            notes=f"Call {row['phone']} for intake hours and required documents before visiting.",
            notes_es=f"Llame al {row['phone']} para horarios de admisión y documentos requeridos.",
            hours="Monday–Friday business hours; program hours vary",
            tags=f"{row['county'].lower()}|basic-needs|emergency-aid|reentry",
            services="Emergency utility assistance|Food assistance|Clothing|Hygiene supplies|Case management referrals",
            county=row["county"],
            served_counties=row["served"],
            coverage="single" if "|" not in row["served"] else "multi",
            _source=row["website"],
            _source_type="nonprofit",
            _confidence="high",
        )

    # --- education (9 more; 3 exist) ---
    _education_rows = [
        ("Washtenaw Community College — Adult Transitions", "Ann Arbor / Washtenaw County", "Washtenaw", "Washtenaw",
         "4800 East Huron River Drive", "Ann Arbor", "734-973-3300", "https://www.wccnet.edu",
         "Washtenaw Community College Adult Transitions program offers GED preparation, high school completion, "
         "and workforce certificate pathways for adult learners including returning citizens in Washtenaw County. "
         "Campus advisors assist with Michigan Reconnect scholarship eligibility and connect students to Michigan Works! "
         "employment partners for fair-chance job placement after credential completion."),
        ("Grand Rapids Community College — Adult Education", "Grand Rapids / Kent County", "Kent", "Kent",
         "143 Bostwick Avenue NE", "Grand Rapids", "616-234-3367", "https://www.grcc.edu",
         "Grand Rapids Community College Adult Education Center provides GED and high school equivalency preparation, "
         "English language instruction, and workforce readiness classes for Kent County adult learners including "
         "justice-involved residents seeking credentials after release. GRCC partners with Michigan Works! West Central "
         "and Offender Success Region 4 for tuition assistance navigation."),
        ("Lansing Community College — High School Diploma Completion", "Lansing / Ingham County", "Ingham", "Ingham",
         "419 North Capitol Avenue", "Lansing", "517-483-1410", "https://www.lcc.edu",
         "Lansing Community College offers adult high school completion, GED preparation, and certificate programs "
         "for Ingham, Eaton, and Clinton county residents including returning citizens rebuilding education after "
         "incarceration. LCC advisors connect eligible students to Michigan Reconnect and Capital Area Michigan Works! "
         "for tuition-free associate degree pathways."),
        ("Macomb Community College — Adult Education", "Warren / Macomb County", "Macomb", "Macomb",
         "14500 East Twelve Mile Road", "Warren", "586-445-7999", "https://www.macomb.edu",
         "Macomb Community College Center for Advanced Training provides GED preparation, adult basic education, "
         "and skilled trades certificate programs for Macomb County adult learners including justice-involved "
         "residents referred by MDOC Offender Success and local courts. Campus career services connect graduates "
         "to southeast Michigan employers."),
        ("Oakland Community College — Adult Education Services", "Bloomfield Hills / Oakland County", "Oakland", "Oakland",
         "2480 Opdyke Road", "Bloomfield Hills", "248-341-2020", "https://www.oaklandcc.edu",
         "Oakland Community College Adult Education Services offers GED preparation, high school completion, "
         "and workforce training for Oakland County residents including returning citizens in metro Detroit suburbs. "
         "OCC advisors assist with Michigan Reconnect eligibility and connect students to Michigan Works! Southeast "
         "and HMSA Offender Success employment partners."),
        ("Kellogg Community College — Adult Education", "Battle Creek / Calhoun County", "Calhoun", "Calhoun|Branch",
         "450 North Avenue", "Battle Creek", "269-965-3931", "https://www.kellogg.edu",
         "Kellogg Community College Adult Education program provides GED preparation, high school completion, "
         "and workforce certificate pathways for Calhoun and Branch county adult learners including returning "
         "citizens in southwest Michigan. KCC partners with Kinexus Offender Success Region 8 and Summit Pointe "
         "for integrated education and recovery support referrals."),
        ("Delta College — Adult Education", "University Center / Bay County", "Bay", "Bay|Saginaw|Midland",
         "1961 Delta Road", "University Center", "989-686-9300", "https://www.delta.edu",
         "Delta College Adult Education offers GED preparation, high school completion, and skilled trades "
         "training for Bay, Saginaw, and Midland county residents including justice-involved individuals "
         "rebuilding credentials in the Great Lakes Bay region. Delta advisors connect students to Michigan Works! "
         "Great Lakes Bay and Michigan Reconnect scholarship programs."),
        ("Kirtland Community College — Adult Education", "Roscommon / Roscommon County", "Roscommon",
         "Alcona|Alpena|Cheboygan|Crawford|Iosco|Montmorency|Ogemaw|Oscoda|Otsego|Presque Isle|Roscommon",
         "10775 North St. Helen Road", "Roscommon", "989-275-5000", "https://www.kirtland.edu",
         "Kirtland Community College serves rural northeast Michigan with GED preparation, adult basic education, "
         "and workforce certificate programs for residents of Roscommon and surrounding counties with thin local "
         "reentry directories. Campus staff assist returning citizens with Michigan Reconnect eligibility and "
         "connect graduates to Michigan Works! Northeast Consortium employment services."),
        ("St. Clair County Community College — Adult Education", "Port Huron / St. Clair County", "St. Clair", "St. Clair",
         "323 Erie Street", "Port Huron", "810-989-5500", "https://www.sc4.edu",
         "St. Clair County Community College Adult Education program offers GED preparation, high school completion, "
         "and workforce training for St. Clair, Sanilac, and Lapeer county residents including returning citizens "
         "in Michigan's Thumb region. SC4 advisors connect students to Michigan Works! East Michigan and local "
         "employers for fair-chance job placement."),
    ]
    for name, region, county, served, address, city, phone, website, desc_en in _education_rows:
        desc_es = (
            desc_en.replace("offers", "ofrece").replace("provides", "proporciona").replace("program", "programa")
            if False else
            f"Programa de educación para adultos de {name.split(' — ')[0]} para residentes de los condados servidos, "
            f"incluidos ciudadanos que regresan que reconstruyen credenciales después de la encarcelación. "
            f"El personal del campus ayuda con elegibilidad Michigan Reconnect y conexiones a Michigan Works!."
        )
        add(
            name=name, category="education", region=region,
            description=desc_en, description_es=desc_es,
            address=address, city=city, phone=phone, email="", website=website,
            eligibility="Michigan adult residents in served counties age 18 and older; criminal record not a stated barrier for adult education.",
            eligibility_es="Residentes adultos de Michigan en condados servidos de 18 años o más; antecedentes penales no son barrera indicada.",
            notes=f"Call {phone} for enrollment; Michigan Reconnect may cover tuition for eligible adults age 25+.",
            notes_es=f"Llame al {phone} para inscripción; Michigan Reconnect puede cubrir matrícula para adultos elegibles de 25+.",
            hours="Campus Mon–Fri; class schedules vary by semester",
            tags=f"{county.lower()}|education|GED|adult-education|reentry",
            services="GED preparation|High school completion|Workforce certificates|Michigan Reconnect navigation|Career services",
            county=county, served_counties=served,
            coverage="single" if "|" not in served else "multi",
            _source=website, _source_type="nonprofit", _confidence="high",
        )

    # --- veterans (7 more; 3 exist) ---
    _veterans_rows = [
        ("Alpena County Veterans Affairs", "Alpena / Alpena County", "Alpena", "Alpena", "320 W. Chisholm Street", "Alpena", "989-354-9870", "https://www.alpenacounty.org"),
        ("Bay County Veterans Services", "Bay City / Bay County", "Bay", "Bay", "515 Center Avenue", "Bay City", "989-895-4280", "https://www.baycounty-mi.gov"),
        ("Calhoun County Veterans Affairs", "Battle Creek / Calhoun County", "Calhoun", "Calhoun", "315 W. Green Street", "Battle Creek", "269-969-6666", "https://www.calhouncountymi.gov"),
        ("Saginaw County Veterans Services", "Saginaw / Saginaw County", "Saginaw", "Saginaw", "111 S. Michigan Avenue", "Saginaw", "989-790-5287", "https://www.saginawcounty.com"),
        ("Tuscola County Veterans Affairs", "Caro / Tuscola County", "Tuscola", "Tuscola", "125 W. Lincoln Street", "Caro", "989-672-8329", "https://www.tuscolacounty.org"),
        ("Kent County Veterans Services", "Grand Rapids / Kent County", "Kent", "Kent", "300 Monroe Avenue NW", "Grand Rapids", "616-632-5725", "https://www.kentcountymi.gov"),
        ("Oakland County Veterans Services", "Pontiac / Oakland County", "Oakland", "Oakland", "1200 N. Telegraph Road", "Pontiac", "248-858-0785", "https://www.oakgov.com"),
    ]
    for name, region, county, served, address, city, phone, website in _veterans_rows:
        desc_en = (
            f"{name} assists county veterans and eligible family members with federal VA disability claims, "
            f"healthcare enrollment, emergency financial assistance, and transportation to VA appointments. "
            f"County veteran service officers serve as local MVAA partners helping justice-involved veterans "
            f"in {county} County access benefits after release from incarceration."
        )
        desc_es = (
            f"{name} ayuda a veteranos del condado y familiares elegibles con reclamaciones de discapacidad "
            f"de la VA, inscripción en atención médica, asistencia financiera de emergencia y transporte a "
            f"citas de la VA. Los oficiales de servicios para veteranos ayudan a veteranos con antecedentes "
            f"penales en el condado {county} a acceder a beneficios después de la liberación."
        )
        add(
            name=name, category="veterans", region=region,
            description=desc_en, description_es=desc_es,
            address=address, city=city, phone=phone, email="", website=website,
            eligibility=f"{county} County veterans and eligible dependents; discharge status affects specific benefit programs.",
            eligibility_es=f"Veteranos del condado {county} y dependientes elegibles; el estado de baja afecta programas específicos.",
            notes="Call for appointment; bring DD-214 and photo ID; connects to VA Medical Center and MVAA statewide resources.",
            notes_es="Llame para cita; traiga DD-214 e identificación; conecta con Centro Médico VA y recursos MVAA.",
            hours="Monday–Friday business hours",
            tags=f"{county.lower()}|veterans|VA-benefits|county|reentry",
            services="VA disability claims assistance|Healthcare enrollment|Emergency financial aid|VA transportation|Benefits counseling",
            county=county, served_counties=served, coverage="single",
            _source=website, _source_type="government", _confidence="high",
        )

    # --- legal-aid (1 more; 11 exist — need 12) ---
    add(
        name="Detroit Justice Center — Civil Legal Services",
        category="legal-aid",
        region="Detroit / Wayne County",
        description=(
            "Nonprofit civil legal services organization representing low-income Wayne County residents "
            "in housing, public benefits, family law, and expungement matters including returning citizens "
            "facing eviction, MI Bridges denials, or civil record barriers to employment. Detroit Justice "
            "Center attorneys provide direct representation in court and assist with Clean Slate expungement "
            "applications—not criminal defense."
        ),
        description_es=(
            "Organización de servicios legales civiles sin fines de lucro que representa a residentes de "
            "bajos ingresos del condado Wayne en vivienda, beneficios públicos, derecho familiar y "
            "eliminación de antecedentes, incluidos ciudadanos que regresan que enfrentan desalojo o "
            "denegaciones de MI Bridges. No proporciona defensa penal."
        ),
        address="7310 Woodward Avenue",
        city="Detroit",
        phone="313-870-9610",
        email="",
        website="https://www.detroitjustice.org",
        eligibility="Low-income Wayne County residents with qualifying civil legal problems; income limits apply; criminal defense not provided.",
        eligibility_es="Residentes de bajos ingresos del condado Wayne con problemas legales civiles calificados; aplican límites de ingresos; no se proporciona defensa penal.",
        notes="Apply at detroitjustice.org or call 313-870-9610; priority for housing and expungement cases affecting reentry.",
        notes_es="Solicite en detroitjustice.org o llame al 313-870-9610; prioridad para casos de vivienda y eliminación de antecedentes.",
        hours="Intake Monday–Friday business hours",
        tags="detroit|wayne|legal-aid|housing|expungement|reentry",
        services="Civil legal representation|Eviction defense|Benefits advocacy|Expungement assistance|Clean Slate applications",
        county="Wayne",
        served_counties="Wayne",
        coverage="single",
        _source="https://www.detroitjustice.org",
        _source_type="nonprofit",
        _confidence="high",
    )

    # --- healthcare (10 more; 10 exist — Alcona + GLB added above = 12, need 8 more) ---
    _healthcare_rows = [
        ("Cherry Health — Federally Qualified Health Center", "Grand Rapids / Kent County", "Kent", "Kent|Barry|Montcalm",
         "550 Cherry Street SE", "Grand Rapids", "616-235-7200", "https://www.cherryhealth.org",
         "Cherry Health operates federally qualified health center sites across Kent and west Michigan providing "
         "primary care, behavioral health, dental, and pharmacy on sliding fee scale for underserved residents "
         "including returning citizens reestablishing medical care after incarceration."),
        ("Hamilton Community Health Network", "Flint / Genesee County", "Genesee", "Genesee|Lapeer|Shiawassee",
         "2900 N. Saginaw Street", "Flint", "810-406-4246", "https://www.hamiltonchn.org",
         "Hamilton Community Health Network is a federally qualified health center serving Genesee, Lapeer, and "
         "Shiawassee counties with primary care, behavioral health, dental, and pharmacy services on sliding "
         "fee scale for Medicaid and uninsured patients including justice-involved Flint-area residents."),
        ("Upper Great Lakes Family Health Center", "Marquette / Upper Peninsula", "Marquette",
         "Alger|Baraga|Chippewa|Delta|Dickinson|Gogebic|Houghton|Iron|Keweenaw|Luce|Mackinac|Marquette|Menominee|Ontonagon|Schoolcraft",
         "508 W. Washington Street", "Marquette", "906-228-9444", "https://www.uglhealth.org",
         "Upper Great Lakes Family Health Center provides federally qualified health center services across all "
         "15 Upper Peninsula counties including primary care, behavioral health, and dental on sliding fee scale "
         "for rural UP residents including returning citizens after release from Marquette Branch Prison."),
        ("Family Health Center of Battle Creek", "Battle Creek / Calhoun County", "Calhoun", "Calhoun",
         "181 W. Emmett Street", "Battle Creek", "269-965-8866", "https://www.fhcbc.org",
         "Family Health Center of Battle Creek is a federally qualified health center providing primary care, "
         "behavioral health, dental, and pharmacy services on sliding fee scale for Calhoun County residents "
         "including justice-involved individuals reestablishing care after release from Calhoun County Jail."),
        ("Health Net of West Michigan", "Grand Rapids / Kent County", "Kent", "Kent",
         "678 Front Avenue NW", "Grand Rapids", "616-726-8200", "https://www.healthnetwm.org",
         "Health Net of West Michigan connects Kent County residents including returning citizens to Medicaid, "
         "Healthy Michigan Plan, and community health resources through enrollment specialists and care navigation. "
         "Staff assist with MI Bridges applications and FQHC referrals for uninsured patients after incarceration."),
        ("Northwest Michigan Health Services", "Benzonia / Northwest Michigan", "Benzie",
         "Antrim|Benzie|Charlevoix|Emmet|Grand Traverse|Kalkaska|Leelanau|Manistee|Missaukee|Wexford",
         "10767 East U.S. 31", "Benzonia", "231-882-4411", "https://www.nmhsi.org",
         "Northwest Michigan Health Services operates federally qualified health center clinics across ten "
         "northwest Lower Michigan counties providing primary care, behavioral health, and dental on sliding "
         "fee scale for rural residents including returning citizens in counties with thin reentry directories."),
        ("MidMichigan Community Health Services", "Harrison / Clare County", "Clare", "Clare|Gladwin|Arenac|Osceola",
         "588 W. Main Street", "Harrison", "989-539-2983", "https://www.midmichiganchs.org",
         "MidMichigan Community Health Services provides primary care and behavioral health on sliding fee scale "
         "for Clare, Gladwin, Arenac, and Osceola county residents including justice-involved individuals in "
         "rural central Michigan reestablishing outpatient care after release."),
        ("McLaren Health Plan — Medicaid Enrollment Assistance", "Flint / Genesee County", "Genesee", "Genesee|Bay|Saginaw",
         "4520 S. Saginaw Street", "Flint", "888-327-0671", "https://www.mclarenhealthplan.org",
         "McLaren Health Plan community enrollment team assists Genesee, Bay, and Saginaw county residents "
         "including returning citizens with Medicaid and Healthy Michigan Plan applications, provider network "
         "navigation, and care coordination after release from incarceration."),
    ]
    for name, region, county, served, address, city, phone, website, desc_en in _healthcare_rows:
        desc_es = (
            f"Centro de salud calificado federalmente o servicio de inscripción en salud que sirve a los "
            f"condados listados con atención primaria, salud conductual y tarifa escalonada para residentes "
            f"desatendidos, incluidos ciudadanos que regresan que restablecen atención médica después de la liberación."
        )
        add(
            name=name, category="healthcare", region=region,
            description=desc_en, description_es=desc_es,
            address=address, city=city, phone=phone, email="", website=website,
            eligibility="Open to residents of served counties; sliding fee or Medicaid based on income; criminal record not a stated barrier.",
            eligibility_es="Abierto a residentes de condados servidos; tarifa escalonada o Medicaid según ingresos.",
            notes=f"Call {phone} for appointments or enrollment assistance; bring ID and release paperwork when establishing care.",
            notes_es=f"Llame al {phone} para citas o ayuda de inscripción; traiga identificación y documentos de liberación.",
            hours="Monday–Friday clinic hours; contact location for schedule",
            tags=f"{county.lower()}|healthcare|FQHC|Medicaid|reentry",
            services="Primary care|Behavioral health|Dental services|Pharmacy|Sliding fee scale|Medicaid enrollment assistance",
            county=county, served_counties=served,
            coverage="single" if "|" not in served else "multi",
            _source=website, _source_type="nonprofit", _confidence="high",
        )

    # --- housing (8 more; 12 exist) ---
    _housing_rows = [
        ("Volunteers of America Michigan — Reentry Housing", "Detroit / Wayne County", "Wayne", "Wayne",
         "3737 Lawton Street", "Detroit", "313-897-1034", "https://www.voami.org",
         "Volunteers of America Michigan operates reentry-focused transitional housing and supportive services "
         "for justice-involved Wayne County residents including men and women paroling from MDOC custody. "
         "Case managers connect residents to employment, treatment, and permanent housing through CAM coordination."),
        ("Community Housing Network — Washtenaw County", "Ann Arbor / Washtenaw County", "Washtenaw", "Washtenaw",
         "106 E. Michigan Avenue", "Ypsilanti", "734-663-5858", "https://www.communityhousingnetwork.org",
         "Community Housing Network provides permanent supportive housing, rapid rehousing, and homelessness "
         "prevention for Washtenaw County residents including returning citizens referred through Coordinated Entry. "
         "Case managers assist with lease applications and MDHHS benefits enrollment."),
        ("Family Promise of Grand Rapids — Shelter & Housing", "Grand Rapids / Kent County", "Kent", "Kent",
         "442 Union Avenue NE", "Grand Rapids", "616-475-5233", "https://www.familypromisegr.org",
         "Family Promise of Grand Rapids provides emergency shelter, transitional housing, and case management "
         "for families experiencing homelessness in Kent County including parents reuniting with children after "
         "incarceration. Congregation-based shelter network with centralized intake."),
        ("Homeless Solutions of Flint & Genesee County", "Flint / Genesee County", "Genesee", "Genesee",
         "519 S. Saginaw Street", "Flint", "810-233-8711", "https://www.homelesssolutions.net",
         "Homeless Solutions operates emergency shelter, rapid rehousing, and permanent supportive housing "
         "programs for Genesee County residents including returning citizens without stable housing after release. "
         "Coordinated Entry intake required for most housing programs."),
        ("Mid-Michigan Coalition to End Homelessness", "Lansing / Ingham County", "Ingham", "Clinton|Eaton|Ingham",
         "330 Marshall Street", "Lansing", "517-482-5555", "https://www.mmceh.org",
         "Mid-Michigan Coalition to End Homelessness coordinates Coordinated Entry and housing navigation "
         "for Clinton, Eaton, and Ingham county residents including justice-involved individuals seeking "
         "emergency shelter, rapid rehousing, or permanent supportive housing in the Lansing area."),
        ("Southwest Michigan Coalition Against Homelessness", "Kalamazoo / Kalamazoo County", "Kalamazoo",
         "Berrien|Branch|Calhoun|Cass|Kalamazoo|St. Joseph|Van Buren",
         "420 E. Alcott Street", "Kalamazoo", "269-382-5644", "https://www.smcahtruth.org",
         "Southwest Michigan Coalition Against Homelessness coordinates housing navigation and Coordinated Entry "
         "for seven southwest Michigan counties including Calhoun, Branch, and St. Joseph where returning citizens "
         "often lack local shelter directories. Connects clients to emergency shelter and rapid rehousing partners."),
        ("NEMCSA — Transitional Housing Program", "Alpena / Northeast Michigan", "Alpena",
         "Alcona|Alpena|Cheboygan|Crawford|Iosco|Montmorency|Ogemaw|Oscoda|Otsego|Presque Isle|Roscommon",
         "2375 Gordon Road", "Alpena", "989-356-3474", "https://www.nemcsa.org",
         "NEMCSA transitional housing program provides short-term housing and case management for low-income "
         "northeast Michigan residents including returning citizens completing Coordinated Entry intake. Separate "
         "from emergency shelter referrals; eligibility requires income documentation and case plan."),
        ("Bay Area Women's Center — Emergency Shelter", "Bay City / Bay County", "Bay", "Bay",
         "809 N. Madison Avenue", "Bay City", "989-686-4551", "https://www.bawc-mi.org",
         "Bay Area Women's Center operates emergency shelter and housing advocacy for survivors of domestic "
         "violence and homelessness in Bay County including women returning from incarceration seeking safe "
         "housing. 24-hour crisis line and confidential intake; also serves families when space available."),
    ]
    for name, region, county, served, address, city, phone, website, desc_en in _housing_rows:
        desc_es = (
            f"Programa de vivienda de emergencia, transicional o de apoyo permanente que sirve a los condados "
            f"listados, incluidos ciudadanos que regresan sin vivienda estable después de la encarcelación. "
            f"La admisión de Entrada Coordinada puede ser requerida; el manejo de casos conecta con empleo y beneficios."
        )
        add(
            name=name, category="housing", region=region,
            description=desc_en, description_es=desc_es,
            address=address, city=city, phone=phone, email="", website=website,
            eligibility="Residents of served counties experiencing homelessness or housing crisis; intake assessment required; criminal record policies vary by program.",
            eligibility_es="Residentes de condados servidos en crisis de vivienda; se requiere evaluación; las políticas de antecedentes varían.",
            notes=f"Call {phone} for intake; Coordinated Entry may be required before shelter placement.",
            notes_es=f"Llame al {phone} para admisión; puede requerirse Entrada Coordinada antes del refugio.",
            hours="Intake Mon–Fri business hours; crisis lines vary",
            tags=f"{county.lower()}|housing|shelter|reentry",
            services="Emergency shelter|Transitional housing|Permanent supportive housing|Rapid rehousing|Case management|Coordinated Entry",
            county=county, served_counties=served,
            coverage="single" if "|" not in served else "multi",
            _source=website, _source_type="nonprofit", _confidence="high",
        )
