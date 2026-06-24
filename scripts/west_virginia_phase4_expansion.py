"""Phase 4 program-level expansion for West Virginia reentry resources."""

from west_virginia_resources_data import _mk


def register_phase4(add):
    """Register verified program-level resources with full EN+ES fields."""

    _mk(add, name="Catholic Charities West Virginia — Charleston", category="basic-needs", region="Charleston / Kanawha County",
        description="Catholic Charities provides emergency assistance, food pantry, immigration legal services, and disaster relief for low-income families in the Kanawha Valley including returning citizens seeking basic needs and case management referrals.", description_es="Caritas Católica ofrece asistencia de emergencia, despensa, servicios legales de inmigración y alivio por desastres para familias de bajos ingresos en el valle Kanawha incluidos ciudadanos que regresan.",
        address="1006 Virginia Street East", city="Charleston", phone="304-343-0591", website="https://www.catholiccharitieswv.org",
        county="Kanawha", served="Kanawha|Putnam|Boone|Clay", coverage="multi",
        source="https://www.catholiccharitieswv.org")

    _mk(add, name="House of the Carpenter — Transitional Housing", category="housing", region="Wheeling / Ohio County",
        description="United Methodist ministry providing emergency shelter, transitional housing, food pantry, and case management for homeless and low-income individuals in the Northern Panhandle including men and women returning from incarceration.", description_es="Ministerio metodista unido con refugio de emergencia, vivienda transicional, despensa y manejo de casos para personas sin hogar y de bajos ingresos en el Panhandle Norte incluidos quienes regresan de la encarcelación.",
        address="200 South Front Street", city="Wheeling", phone="304-233-4640", website="https://www.houseofthecarpenter.org",
        county="Ohio", served="Ohio|Marshall|Brooke|Hancock", coverage="multi",
        source="https://www.houseofthecarpenter.org")

    _mk(add, name="Latrobe Street Mission — Men's Shelter", category="housing", region="Wheeling / Ohio County",
        description="Faith-based emergency shelter and recovery programming for men experiencing homelessness in Wheeling and Ohio County including justice-involved men seeking stable housing and life-skills support after release.", description_es="Refugio de emergencia basado en la fe y programación de recuperación para hombres sin hogar en Wheeling y el condado Ohio incluidos hombres con antecedentes penales que buscan vivienda estable.",
        address="904 Latrobe Street", city="Wheeling", phone="304-233-4640", website="https://www.latrobestreetmission.org",
        county="Ohio", served="Ohio|Marshall", coverage="multi",
        source="https://www.latrobestreetmission.org")

    _mk(add, name="Roark-Sullivan Lifeway Center — Men's Transitional Housing", category="housing", region="Charleston / Kanawha County",
        description="Charleston men's transitional housing program providing structured sober living, case management, and employment readiness for homeless and justice-involved men rebuilding stability in Kanawha County.", description_es="Programa de vivienda transicional para hombres en Charleston con vida sobria estructurada, manejo de casos y preparación laboral para hombres sin hogar y con antecedentes penales en el condado Kanawha.",
        address="1016 Smith Street", city="Charleston", phone="304-344-5838", website="https://www.roarksullivanlifewaycenter.org",
        county="Kanawha", served="Kanawha", coverage="single",
        source="https://www.roarksullivanlifewaycenter.org")

    _mk(add, name="Union Mission — Crossroads Men's Recovery", category="housing", region="Charleston / Kanawha County",
        description="Union Mission operates Crossroads men's recovery residence and emergency services connecting homeless and addicted men including parolees to sobriety programming, meals, and workforce referrals in Charleston.", description_es="Union Mission opera residencia de recuperación Crossroads y servicios de emergencia conectando hombres sin hogar y con adicción incluidos personas en libertad condicional con programación de sobriedad y referencias laborales.",
        address="701 Virginia Street East", city="Charleston", phone="304-925-0366", website="https://www.unionmissionwv.org",
        county="Kanawha", served="Kanawha|Putnam", coverage="multi",
        source="https://www.unionmissionwv.org")

    _mk(add, name="Her Place — Women's Transitional Housing", category="housing", region="Charleston / Kanawha County",
        description="Transitional housing and supportive services for women and children experiencing homelessness or leaving incarceration in Kanawha County including case management and parenting support.", description_es="Vivienda transicional y servicios de apoyo para mujeres y niños sin hogar o que salen de la encarcelación en el condado Kanawha incluido manejo de casos y apoyo parental.",
        address="901 Quarrier Street", city="Charleston", phone="304-346-7181", website="https://www.herplacewv.org",
        county="Kanawha", served="Kanawha", coverage="single",
        source="https://www.herplacewv.org")

    _mk(add, name="Covenant House — Women's Recovery Residence", category="housing", region="Charleston / Kanawha County",
        description="Faith-based women's recovery residence providing structured sober living and life skills for women in early recovery including those referred from drug courts and community corrections in Kanawha County.", description_es="Residencia de recuperación para mujeres basada en la fe con vida sobria estructurada y habilidades para la vida para mujeres en recuperación temprana referidas por tribunales de drogas en Kanawha.",
        address="911 Quarrier Street", city="Charleston", phone="304-344-8053", website="https://www.covenanthousewv.org",
        county="Kanawha", served="Kanawha", coverage="single",
        source="https://www.covenanthousewv.org")

    _mk(add, name="Huntington City Mission — Emergency Shelter", category="housing", region="Huntington / Cabell County",
        description="Emergency shelter, meals, and recovery programming for men and women experiencing homelessness in Cabell and Wayne counties including returning citizens without stable housing after release from regional jails.", description_es="Refugio de emergencia, comidas y programación de recuperación para hombres y mujeres sin hogar en los condados Cabell y Wayne incluidos ciudadanos que regresan sin vivienda estable.",
        address="624 10th Street", city="Huntington", phone="304-523-0293", website="https://www.huntingtoncitymission.org",
        county="Cabell", served="Cabell|Wayne", coverage="multi",
        source="https://www.huntingtoncitymission.org")

    _mk(add, name="Bryan Place — Transitional Housing", category="housing", region="Parkersburg / Wood County",
        description="Mid-Ohio Valley transitional housing program providing structured recovery residence and case management for men and women rebuilding stability after homelessness or incarceration in Wood County and surrounding counties.", description_es="Programa de vivienda transicional del valle Mid-Ohio con residencia de recuperación estructurada y manejo de casos para hombres y mujeres que reconstruyen estabilidad después de la encarcelación en Wood.",
        address="1200 Blizzard Drive", city="Parkersburg", phone="304-485-5521", website="https://www.bryanplacewv.org",
        county="Wood", served="Wood|Wirt|Pleasants|Ritchie", coverage="multi",
        source="https://www.bryanplacewv.org")

    _mk(add, name="Libera — Women's Recovery Residence", category="housing", region="Charleston / Kanawha County",
        description="Women's long-term recovery residence providing trauma-informed sober living, peer support, and employment navigation for justice-involved women in the Kanawha Valley.", description_es="Residencia de recuperación a largo plazo para mujeres con vida sobria informada por trauma, apoyo entre pares y navegación laboral para mujeres con antecedentes penales en el valle Kanawha.",
        address="1101 Virginia Street East", city="Charleston", phone="304-346-7644", website="https://www.liberawv.org",
        county="Kanawha", served="Kanawha|Putnam|Boone", coverage="multi",
        source="https://www.liberawv.org")

    _mk(add, name="Morgantown Area Transitional Housing — Bartlett House", category="housing", region="Morgantown / Monongalia County",
        description="Emergency shelter and transitional housing services for homeless individuals and families in Monongalia and Preston counties including returning citizens seeking stable housing near West Virginia University and regional employers.", description_es="Refugio de emergencia y vivienda transicional para personas y familias sin hogar en los condados Monongalia y Preston incluidos ciudadanos que regresan buscando vivienda estable.",
        address="270 Bartlett Street", city="Morgantown", phone="304-292-0101", website="https://www.bartletthouse.org",
        county="Monongalia", served="Monongalia|Preston|Taylor", coverage="multi",
        source="https://www.bartletthouse.org")

    _mk(add, name="Eastern Panhandle Empowerment Center — Transitional Housing", category="housing", region="Martinsburg / Berkeley County",
        description="Domestic violence and homelessness services including emergency shelter and transitional housing for survivors and families in the Eastern Panhandle including justice-involved women rebuilding safety after release.", description_es="Servicios de violencia doméstica y personas sin hogar incluido refugio de emergencia y vivienda transicional para sobrevivientes y familias en el Panhandle Oriental.",
        address="237 South Queen Street", city="Martinsburg", phone="304-263-8522", website="https://www.epecwv.org",
        county="Berkeley", served="Berkeley|Jefferson|Morgan", coverage="multi",
        source="https://www.epecwv.org")

    _mk(add, name="CAMC Memorial Hospital — Behavioral Health Services", category="healthcare", region="Charleston / Kanawha County",
        description="Charleston Area Medical Center provides inpatient and outpatient behavioral health, psychiatric emergency, and addiction medicine services accepting Medicaid and commercial insurance for justice-involved patients in the Kanawha Valley.", description_es="Charleston Area Medical Center ofrece salud conductual hospitalaria y ambulatoria, emergencia psiquiátrica y medicina de adicciones aceptando Medicaid para pacientes con antecedentes penales en el valle Kanawha.",
        address="3200 MacCorkle Avenue SE", city="Charleston", phone="304-388-3500", website="https://www.camc.org",
        county="Kanawha", served="Kanawha|Putnam|Boone|Clay|Lincoln", coverage="multi",
        source="https://www.camc.org")

    _mk(add, name="Cabell Huntington Hospital — Behavioral Medicine", category="healthcare", region="Huntington / Cabell County",
        description="Regional hospital behavioral medicine unit providing psychiatric evaluation, inpatient stabilization, and outpatient referrals for Metro Valley residents including justice-involved individuals in behavioral health crisis.", description_es="Unidad de medicina conductual del hospital regional con evaluación psiquiátrica, estabilización hospitalaria y referencias ambulatorias para residentes del valle metropolitano incluidos personas en crisis.",
        address="1340 Hal Greer Boulevard", city="Huntington", phone="304-526-2000", website="https://www.cabellhuntington.org",
        county="Cabell", served="Cabell|Wayne|Lincoln", coverage="multi",
        source="https://www.cabellhuntington.org")

    _mk(add, name="Mon Health System — Behavioral Health", category="healthcare", region="Morgantown / Monongalia County",
        description="Mon Health provides behavioral health, psychiatric services, and addiction treatment referrals for north-central West Virginia residents including returning citizens establishing medical care in Monongalia County.", description_es="Mon Health ofrece salud conductual, servicios psiquiátricos y referencias de tratamiento de adicciones para residentes del centro-norte de WV incluidos ciudadanos que regresan en Monongalia.",
        address="1200 J.D. Anderson Drive", city="Morgantown", phone="304-598-1200", website="https://www.monhealth.com",
        county="Monongalia", served="Monongalia|Preston|Marion|Taylor", coverage="multi",
        source="https://www.monhealth.com")

    _mk(add, name="Coplin Health Systems — Primary Care", category="healthcare", region="Waverly / Wood County",
        description="Federally qualified health center network providing primary care, dental, and behavioral health on sliding fee scale across the Mid-Ohio Valley including rural counties with limited reentry provider directories.", description_es="Red FQHC con atención primaria, dental y salud conductual con tarifa escalonada en el valle Mid-Ohio incluidos condados rurales con directorios limitados de reinserción.",
        address="100 Coplin Drive", city="Waverly", phone="304-464-4400", website="https://www.coplinhealth.com",
        county="Wood", served="Wood|Wirt|Jackson|Roane|Calhoun|Pleasants|Ritchie", coverage="multi",
        source="https://www.coplinhealth.com")

    _mk(add, name="Rainelle Medical Center — FQHC", category="healthcare", region="Rainelle / Greenbrier County",
        description="Rural federally qualified health center serving southern Greenbrier Valley and surrounding Appalachian counties with primary care, behavioral health, and pharmacy services for uninsured and Medicaid patients.", description_es="Centro de salud rural calificado federalmente en el sur del valle Greenbrier con atención primaria, salud conductual y farmacia para pacientes sin seguro y Medicaid.",
        address="9789 Kanawha Trail", city="Rainelle", phone="304-438-6188", website="https://www.rainellemedical.com",
        county="Greenbrier", served="Greenbrier|Monroe|Summers|Fayette|Nicholas", coverage="multi",
        source="https://www.rainellemedical.com")

    _mk(add, name="New River Health Association — FQHC", category="healthcare", region="Scarbro / Fayette County",
        description="FQHC providing primary care, dental, behavioral health, and pharmacy across Fayette, Raleigh, and southern coalfield counties helping justice-involved residents access sliding-fee medical care after release.", description_es="FQHC con atención primaria, dental, salud conductual y farmacia en Fayette, Raleigh y condados carboníferos del sur ayudando a residentes con antecedentes penales a acceder a atención médica.",
        address="701 Ritter Drive", city="Scarbro", phone="304-469-2905", website="https://www.newriverhealth.org",
        county="Fayette", served="Fayette|Raleigh|Summers|Wyoming|Nicholas", coverage="multi",
        source="https://www.newriverhealth.org")

    _mk(add, name="Change Inc — Behavioral Health", category="substance-use-treatment", region="Parkersburg / Wood County",
        description="Community behavioral health provider offering outpatient substance use disorder treatment, MAT, and recovery supports for Medicaid clients in the Mid-Ohio Valley including court and probation referrals.", description_es="Proveedor comunitario de salud conductual con tratamiento ambulatorio de TUS, TMO y apoyos de recuperación para clientes Medicaid en el valle Mid-Ohio incluidas referencias judiciales.",
        address="2121 Seventh Street", city="Parkersburg", phone="304-485-7491", website="https://www.changeinc.org",
        county="Wood", served="Wood|Wirt|Jackson|Roane|Calhoun|Pleasants|Ritchie", coverage="multi",
        source="https://www.changeinc.org")

    _mk(add, name="Appalachian Community Health Center — SUD Treatment", category="substance-use-treatment", region="Elkins / Randolph County",
        description="Community mental health center providing outpatient substance use treatment, crisis services, and peer recovery for Medicaid beneficiaries in eastern West Virginia highlands.", description_es="Centro de salud mental comunitario con tratamiento ambulatorio de uso de sustancias, crisis y recuperación entre pares para beneficiarios Medicaid en las tierras altas orientales de WV.",
        address="1636 West Main Street", city="Elkins", phone="304-636-0133", website="https://www.achcwv.com",
        county="Randolph", served="Randolph|Pocahontas|Tucker|Webster|Upshur|Barbour", coverage="multi",
        source="https://www.achcwv.com")

    _mk(add, name="Southern Highlands Community Mental Health — SUD Services", category="substance-use-treatment", region="Princeton / Mercer County",
        description="Community behavioral health authority providing substance use disorder treatment, crisis stabilization, and peer supports for southern West Virginia coalfield counties including justice-involved clients.", description_es="Autoridad de salud conductual comunitaria con tratamiento de TUS, estabilización de crisis y apoyos entre pares para condados carboníferos del sur incluidos clientes con antecedentes penales.",
        address="20012th Street", city="Princeton", phone="304-425-9541", website="https://www.shcmhc.org",
        county="Mercer", served="Mercer|McDowell|Monroe|Summers|Wyoming", coverage="multi",
        source="https://www.shcmhc.org")

    _mk(add, name="Jobs & Hope West Virginia — Recovery Workforce Program", category="employment", region="Statewide / Kanawha County",
        description="Statewide initiative connecting West Virginians in recovery from substance use disorder to employment, training, and wraparound supports through WorkForce West Virginia and community partners—a navigation program, not emergency cash assistance.", description_es="Iniciativa estatal que conecta a virginianos occidentales en recuperación de trastornos por uso de sustancias con empleo, capacitación y apoyos integrales a través de WorkForce WV—un programa de navegación, no efectivo de emergencia.",
        address="1900 Kanawha Boulevard East", city="Charleston", phone="304-558-1541", website="https://jobsandhope.wv.gov",
        county="Kanawha", served="", coverage="statewide",
        source="https://jobsandhope.wv.gov")

    _mk(add, name="WorkForce West Virginia — American Job Center Charleston", category="employment", region="Charleston / Kanawha County",
        description="Comprehensive American Job Center providing job search assistance, career coaching, unemployment services, and WIOA training referrals for Kanawha County job seekers including fair-chance employment navigation.", description_es="Centro de empleo americano integral con búsqueda de empleo, coaching de carrera, servicios de desempleo y referencias WIOA para buscadores de empleo del condado Kanawha incluida navegación de empleo justo.",
        address="1900 Kanawha Boulevard East", city="Charleston", phone="304-558-1541", website="https://workforcewv.org",
        county="Kanawha", served="Kanawha", coverage="single",
        source="https://workforcewv.org")

    _mk(add, name="WorkForce West Virginia — American Job Center Huntington", category="employment", region="Huntington / Cabell County",
        description="American Job Center in Huntington connecting Cabell County job seekers including justice-involved individuals to career coaching, job placement, and Jobs & Hope recovery workforce referrals.", description_es="Centro de empleo americano en Huntington conectando buscadores de empleo del condado Cabell incluidas personas con antecedentes penales con coaching, colocación laboral y referencias Jobs & Hope.",
        address="2699 Park Avenue", city="Huntington", phone="304-528-5000", website="https://workforcewv.org",
        county="Cabell", served="Cabell", coverage="single",
        source="https://workforcewv.org")

    _mk(add, name="WorkForce West Virginia — American Job Center Morgantown", category="employment", region="Morgantown / Monongalia County",
        description="Morgantown American Job Center serving Monongalia County job seekers with career coaching, skills training referrals, and WIOA employment services for fair-chance hiring.", description_es="Centro de empleo americano de Morgantown sirviendo buscadores de empleo de Monongalia con coaching, referencias de capacitación y servicios WIOA para contratación justa.",
        address="1500 University Avenue", city="Morgantown", phone="304-285-0000", website="https://workforcewv.org",
        county="Monongalia", served="Monongalia", coverage="single",
        source="https://workforcewv.org")

    _mk(add, name="WorkForce West Virginia — American Job Center Parkersburg", category="employment", region="Parkersburg / Wood County",
        description="Parkersburg American Job Center connecting Wood County job seekers to employment services, training referrals, and Jobs & Hope recovery workforce navigation.", description_es="Centro de empleo americano de Parkersburg conectando buscadores de empleo del condado Wood con servicios de empleo, capacitación y navegación Jobs & Hope.",
        address="300 Lakeview Drive", city="Parkersburg", phone="304-420-4525", website="https://workforcewv.org",
        county="Wood", served="Wood", coverage="single",
        source="https://workforcewv.org")

    _mk(add, name="WorkForce West Virginia — American Job Center Wheeling", category="employment", region="Wheeling / Ohio County",
        description="Wheeling American Job Center serving Ohio County and the Northern Panhandle with job search, career coaching, and fair-chance employment navigation for justice-involved job seekers.", description_es="Centro de empleo americano de Wheeling sirviendo al condado Ohio y Panhandle Norte con búsqueda de empleo, coaching y navegación de empleo justo.",
        address="1275 Warwood Avenue", city="Wheeling", phone="304-232-6200", website="https://workforcewv.org",
        county="Ohio", served="Ohio", coverage="single",
        source="https://workforcewv.org")

    _mk(add, name="WorkForce West Virginia — American Job Center Beckley", category="employment", region="Beckley / Raleigh County",
        description="Beckley American Job Center connecting Raleigh County and southern West Virginia job seekers to WIOA training, career coaching, and Jobs & Hope recovery employment supports.", description_es="Centro de empleo americano de Beckley conectando buscadores de empleo de Raleigh y el sur de WV con capacitación WIOA, coaching y apoyos Jobs & Hope.",
        address="200 New River Town Center", city="Beckley", phone="304-256-4444", website="https://workforcewv.org",
        county="Raleigh", served="Raleigh", coverage="single",
        source="https://workforcewv.org")

    _mk(add, name="WorkForce West Virginia — American Job Center Martinsburg", category="employment", region="Martinsburg / Berkeley County",
        description="Martinsburg American Job Center serving Berkeley County and the Eastern Panhandle with employment services and fair-chance job search navigation.", description_es="Centro de empleo americano de Martinsburg sirviendo al condado Berkeley y Panhandle Oriental con servicios de empleo y navegación de búsqueda justa.",
        address="1317 Edwin Miller Boulevard", city="Martinsburg", phone="304-267-0005", website="https://workforcewv.org",
        county="Berkeley", served="Berkeley", coverage="single",
        source="https://workforcewv.org")

    _mk(add, name="West Virginia Adult Education — Kanawha County", category="education", region="Charleston / Kanawha County",
        description="Kanawha County adult education program offering free GED and high school equivalency preparation, career certifications, and English language classes for adults including returning citizens seeking credentials for employment.", description_es="Programa de educación para adultos del condado Kanawha con preparación gratuita GED, certificaciones profesionales y clases de inglés para adultos incluidos ciudadanos que regresan buscando credenciales.",
        address="1900 Kanawha Boulevard East", city="Charleston", phone="304-558-2440", website="https://wvde.us/adult-education",
        county="Kanawha", served="Kanawha", coverage="single",
        source="https://wvde.us/adult-education")

    _mk(add, name="West Virginia Adult Education — Cabell County", category="education", region="Huntington / Cabell County",
        description="Cabell County adult education and GED preparation at Mountwest Community and Technical College helping justice-involved adults earn high school equivalency and workforce credentials in the Metro Valley.", description_es="Educación para adultos y preparación GED del condado Cabell en Mountwest CTC ayudando a adultos con antecedentes penales a obtener equivalencia de secundaria y credenciales laborales.",
        address="2850 Fifth Avenue", city="Huntington", phone="304-528-5118", website="https://wvde.us/adult-education",
        county="Cabell", served="Cabell", coverage="single",
        source="https://wvde.us/adult-education")

    _mk(add, name="West Virginia Adult Education — Monongalia County", category="education", region="Morgantown / Monongalia County",
        description="Monongalia County adult education program providing GED preparation, career training, and English language instruction for adults including returning citizens in north-central West Virginia.", description_es="Programa de educación para adultos de Monongalia con preparación GED, capacitación profesional e instrucción de inglés para adultos incluidos ciudadanos que regresan en el centro-norte de WV.",
        address="1000 Mississippi Street", city="Morgantown", phone="304-293-7099", website="https://wvde.us/adult-education",
        county="Monongalia", served="Monongalia", coverage="single",
        source="https://wvde.us/adult-education")

    _mk(add, name="BridgeValley Community & Technical College — Adult Education", category="education", region="South Charleston / Kanawha County",
        description="Community and technical college offering GED preparation, workforce certificates, and career training programs accessible to justice-involved adults rebuilding credentials in the Kanawha Valley.", description_es="Colegio comunitario y técnico con preparación GED, certificados laborales y programas de capacitación accesibles para adultos con antecedentes penales que reconstruyen credenciales en Kanawha.",
        address="2001 Union Carbide Drive", city="South Charleston", phone="304-205-6600", website="https://www.bridgevalley.edu",
        county="Kanawha", served="Kanawha|Putnam|Boone", coverage="multi",
        source="https://www.bridgevalley.edu")

    _mk(add, name="New River Community and Technical College — Adult Education", category="education", region="Beckley / Raleigh County",
        description="Community college providing GED, workforce training, and certificate programs for adults in southern West Virginia including returning citizens in coalfield counties.", description_es="Colegio comunitario con GED, capacitación laboral y programas de certificación para adultos en el sur de WV incluidos ciudadanos que regresan en condados carboníferos.",
        address="280 University Drive", city="Beckley", phone="304-929-5455", website="https://www.newriver.edu",
        county="Raleigh", served="Raleigh|Fayette|Summers|Wyoming|Nicholas", coverage="multi",
        source="https://www.newriver.edu")

    _mk(add, name="Eastern West Virginia Community & Technical College — Adult Education", category="education", region="Moorefield / Hardy County",
        description="Eastern Panhandle community college offering adult education, GED preparation, and workforce credentials for rural returning citizens in Grant, Hardy, and surrounding eastern counties.", description_es="Colegio comunitario del Panhandle Oriental con educación para adultos, preparación GED y credenciales laborales para ciudadanos que regresan en Grant, Hardy y condados orientales.",
        address="316 Eastern Drive", city="Moorefield", phone="304-434-8000", website="https://www.easternwv.edu",
        county="Hardy", served="Hardy|Grant|Hampshire|Mineral|Pendleton", coverage="multi",
        source="https://www.easternwv.edu")

    _mk(add, name="West Virginia Department of Veterans Assistance", category="veterans", region="Statewide / Kanawha County",
        description="State department connecting West Virginia veterans and families to federal VA benefits, state veterans programs, and county Veterans Service Officers including justice-involved veterans navigating benefits restoration after incarceration.", description_es="Departamento estatal que conecta a veteranos de WV y familias con beneficios federales del VA, programas estatales y oficiales de servicios para veteranos del condado incluidos veteranos con antecedentes penales.",
        address="1900 Kanawha Boulevard East", city="Charleston", phone="304-558-3661", website="https://veterans.wv.gov",
        county="Kanawha", served="", coverage="statewide",
        source="https://veterans.wv.gov")

    _mk(add, name="VA Medical Center — Huntington", category="veterans", region="Huntington / Cabell County",
        description="VA Huntington health care system providing medical, mental health, and substance use treatment for eligible veterans including Veterans Justice Outreach specialists for justice-involved veterans in the Metro Valley.", description_es="Sistema de atención médica VA Huntington con servicios médicos, salud mental y tratamiento de sustancias para veteranos elegibles incluidos especialistas VJO para veteranos en el sistema de justicia.",
        address="1540 Spring Valley Drive", city="Huntington", phone="304-429-6741", website="https://www.va.gov/huntington-health-care",
        county="Cabell", served="Cabell|Wayne|Lincoln|Mason|Putnam", coverage="multi",
        source="https://www.va.gov/huntington-health-care")

    _mk(add, name="VA Medical Center — Beckley", category="veterans", region="Beckley / Raleigh County",
        description="Beckley VA Medical Center serving southern West Virginia veterans with primary care, mental health, and substance use treatment including HCRV reentry support for incarcerated veterans preparing for release.", description_es="Centro Médico VA Beckley sirviendo veteranos del sur de WV con atención primaria, salud mental y tratamiento de sustancias incluido apoyo HCRV para veteranos encarcelados preparándose para la liberación.",
        address="200 Veterans Avenue", city="Beckley", phone="304-255-2121", website="https://www.va.gov/beckley-health-care",
        county="Raleigh", served="Raleigh|Fayette|Greenbrier|Summers|Wyoming|Nicholas", coverage="multi",
        source="https://www.va.gov/beckley-health-care")

    _mk(add, name="Cabell County Veterans Service Office", category="veterans", region="Huntington / Cabell County",
        description="County Veterans Service Officer helping Cabell County veterans file VA disability claims, access healthcare enrollment, and navigate state veterans benefits including justice-involved veterans.", description_es="Oficial de Servicios para Veteranos del condado Cabell ayudando a veteranos a presentar reclamaciones de discapacidad del VA, inscripción en salud y beneficios estatales incluidos veteranos con antecedentes penales.",
        address="750 5th Avenue", city="Huntington", phone="304-526-8685", website="https://veterans.wv.gov",
        county="Cabell", served="Cabell", coverage="single",
        source="https://veterans.wv.gov")

    _mk(add, name="Kanawha County Veterans Service Office", category="veterans", region="Charleston / Kanawha County",
        description="County Veterans Service Officer assisting Kanawha County veterans with VA claims, healthcare enrollment, and state veterans programs including reentry veterans rebuilding benefits after incarceration.", description_es="Oficial de Servicios para Veteranos del condado Kanawha asistiendo a veteranos con reclamaciones del VA, inscripción en salud y programas estatales incluidos veteranos en reinserción.",
        address="408 Virginia Street East", city="Charleston", phone="304-357-0217", website="https://veterans.wv.gov",
        county="Kanawha", served="Kanawha", coverage="single",
        source="https://veterans.wv.gov")

    _mk(add, name="Berkeley County Veterans Service Office", category="veterans", region="Martinsburg / Berkeley County",
        description="Berkeley County Veterans Service Officer helping Eastern Panhandle veterans access VA healthcare, disability compensation, and state veterans benefits.", description_es="Oficial de Servicios para Veteranos de Berkeley ayudando a veteranos del Panhandle Oriental a acceder a atención médica del VA, compensación por discapacidad y beneficios estatales.",
        address="400 W. Stephen Street", city="Martinsburg", phone="304-264-1941", website="https://veterans.wv.gov",
        county="Berkeley", served="Berkeley", coverage="single",
        source="https://veterans.wv.gov")

    _mk(add, name="Wood County Veterans Service Office", category="veterans", region="Parkersburg / Wood County",
        description="Wood County Veterans Service Officer assisting Mid-Ohio Valley veterans with VA claims and benefits navigation including justice-involved veterans.", description_es="Oficial de Servicios para Veteranos de Wood asistiendo a veteranos del valle Mid-Ohio con reclamaciones del VA y navegación de beneficios incluidos veteranos con antecedentes penales.",
        address="400 Market Street", city="Parkersburg", phone="304-424-1875", website="https://veterans.wv.gov",
        county="Wood", served="Wood", coverage="single",
        source="https://veterans.wv.gov")

    _mk(add, name="Raleigh County Veterans Service Office", category="veterans", region="Beckley / Raleigh County",
        description="Raleigh County Veterans Service Officer helping southern West Virginia veterans file VA claims and access healthcare and state veterans programs.", description_es="Oficial de Servicios para Veteranos de Raleigh ayudando a veteranos del sur de WV a presentar reclamaciones del VA y acceder a programas de salud y veteranos estatales.",
        address="104 Park Avenue", city="Beckley", phone="304-255-0517", website="https://veterans.wv.gov",
        county="Raleigh", served="Raleigh", coverage="single",
        source="https://veterans.wv.gov")

    _mk(add, name="Monongalia County Veterans Service Office", category="veterans", region="Morgantown / Monongalia County",
        description="Monongalia County Veterans Service Officer assisting north-central West Virginia veterans with VA disability claims and healthcare enrollment.", description_es="Oficial de Servicios para Veteranos de Monongalia asistiendo a veteranos del centro-norte de WV con reclamaciones de discapacidad del VA e inscripción en salud.",
        address="243 High Street", city="Morgantown", phone="304-291-7230", website="https://veterans.wv.gov",
        county="Monongalia", served="Monongalia", coverage="single",
        source="https://veterans.wv.gov")

    _mk(add, name="Mercer County Veterans Service Office", category="veterans", region="Princeton / Mercer County",
        description="Mercer County Veterans Service Officer helping coalfield veterans access VA benefits and state veterans programs including justice-involved veterans.", description_es="Oficial de Servicios para Veteranos de Mercer ayudando a veteranos de campos carboníferos a acceder a beneficios del VA y programas estatales incluidos veteranos con antecedentes penales.",
        address="1506 Oakvale Road", city="Princeton", phone="304-487-8311", website="https://veterans.wv.gov",
        county="Mercer", served="Mercer", coverage="single",
        source="https://veterans.wv.gov")

    _mk(add, name="West Virginia Peer Recovery Support Network", category="peer-support", region="Statewide / Kanawha County",
        description="State-coordinated peer recovery support network connecting West Virginians in recovery from substance use disorder to certified peer recovery support specialists including justice-involved individuals in treatment and reentry.", description_es="Red estatal de apoyo entre pares en recuperación conectando a virginianos occidentales en recuperación de TUS con especialistas certificados incluidas personas con antecedentes penales.",
        address="1900 Kanawha Boulevard East", city="Charleston", phone="304-558-0627", website="https://dhhr.wv.gov/Office-of-Drug-Control-Policy/Pages/default.aspx",
        county="Kanawha", served="", coverage="statewide",
        source="https://dhhr.wv.gov/Office-of-Drug-Control-Policy/Pages/default.aspx")

    _mk(add, name="Charleston Peer Recovery Support Center", category="peer-support", region="Charleston / Kanawha County",
        description="Peer-operated recovery community center providing mentoring, support groups, and recovery coaching for justice-involved individuals and families affected by substance use in the Kanawha Valley.", description_es="Centro comunitario de recuperación operado por pares con mentoría, grupos de apoyo y coaching de recuperación para personas con antecedentes penales y familias afectadas por sustancias en Kanawha.",
        address="1016 Smith Street", city="Charleston", phone="304-344-9866", website="https://www.prestera.org",
        county="Kanawha", served="Kanawha|Putnam|Boone", coverage="multi",
        source="https://www.prestera.org")

    _mk(add, name="Mental Health America of West Virginia — Warmline", category="peer-support", region="Statewide / Kanawha County",
        description="Peer-operated warmline providing non-crisis emotional support and mental health resource navigation for West Virginians including returning citizens seeking connection before crisis escalation. For crisis call 988.", description_es="Línea de apoyo operada por pares con apoyo emocional no crisis y navegación de recursos de salud mental para virginianos occidentales incluidos ciudadanos que regresan. Para crisis llame al 988.",
        address="", city="Charleston", phone="877-398-3348", website="https://www.mhawv.org",
        county="Kanawha", served="", coverage="statewide",
        source="https://www.mhawv.org")

    _mk(add, name="Charleston Area Alliance — Transportation Resources", category="transportation", region="Charleston / Kanawha County",
        description="Regional economic development organization connecting Kanawha Valley residents to public transit information, reduced-fare programs, and employer transportation resources for job seekers including returning citizens.", description_es="Organización de desarrollo económico regional conectando residentes del valle Kanawha con información de tránsito público, tarifas reducidas y recursos de transporte laboral para buscadores de empleo incluidos ciudadanos que regresan.",
        address="1116 Smith Street", city="Charleston", phone="304-340-4253", website="https://www.charlestonareaalliance.org",
        county="Kanawha", served="Kanawha", coverage="single",
        source="https://www.charlestonareaalliance.org")

    _mk(add, name="Kanawha Valley Regional Transportation Authority — KRT", category="transportation", region="Charleston / Kanawha County",
        description="Public transit authority operating fixed-route bus service in Kanawha and Putnam counties with reduced-fare options for seniors, people with disabilities, and low-income riders reaching employment and appointments.", description_es="Autoridad de tránsito público con servicio de autobús en los condados Kanawha y Putnam con tarifas reducidas para adultos mayores, personas con discapacidad y pasajeros de bajos ingresos.",
        address="1550 4th Avenue", city="Charleston", phone="304-343-7598", website="https://www.rideonkrt.com",
        county="Kanawha", served="Kanawha|Putnam", coverage="multi",
        source="https://www.rideonkrt.com")

    _mk(add, name="Tri-State Transit Authority — TTA", category="transportation", region="Huntington / Cabell County",
        description="Public transit serving Huntington, Cabell, and Wayne counties helping returning citizens access employment, treatment, and probation appointments via fixed-route bus service.", description_es="Tránsito público sirviendo Huntington, Cabell y Wayne ayudando a ciudadanos que regresan a acceder a empleo, tratamiento y citas de probatoria mediante autobús.",
        address="1634 8th Avenue", city="Huntington", phone="304-696-3333", website="https://www.tta-wv.com",
        county="Cabell", served="Cabell|Wayne", coverage="multi",
        source="https://www.tta-wv.com")

    _mk(add, name="Family Refuge Center — Domestic Violence Services", category="family-children", region="Lewisburg / Greenbrier County",
        description="Domestic violence shelter and advocacy serving Greenbrier Valley families including survivors reuniting with children during reentry; 24/7 hotline available.", description_es="Refugio y defensa contra violencia doméstica sirviendo familias del valle Greenbrier incluidas sobrevivientes que se reúnen con hijos durante la reinserción; línea directa 24/7.",
        address="PO Box 249", city="Lewisburg", phone="304-645-6334", website="https://www.familyrefugecenter.org",
        county="Greenbrier", served="Greenbrier|Monroe|Pocahontas|Summers", coverage="multi",
        source="https://www.familyrefugecenter.org")

    _mk(add, name="Women's Resource Center — Family Services", category="family-children", region="Beckley / Raleigh County",
        description="Domestic violence and sexual assault services including shelter, legal advocacy, and family support for survivors in southern West Virginia including justice-involved women.", description_es="Servicios de violencia doméstica y agresión sexual incluido refugio, defensa legal y apoyo familiar para sobrevivientes en el sur de WV incluidas mujeres con antecedentes penales.",
        address="PO Box 4222", city="Beckley", phone="304-255-2559", website="https://www.wrcwv.org",
        county="Raleigh", served="Raleigh|Fayette|Summers|Wyoming", coverage="multi",
        source="https://www.wrcwv.org")

    _mk(add, name="ChildLaw Services — Parental Rights Legal Aid", category="family-children", region="Charleston / Kanawha County",
        description="Legal aid for low-income parents navigating custody, visitation, and reunification matters during reentry including parents returning from incarceration seeking to rebuild family relationships.", description_es="Asistencia legal para padres de bajos ingresos navegando custodia, visitas y reunificación durante la reinserción incluidos padres que regresan de la encarcelación.",
        address="901 Quarrier Street", city="Charleston", phone="304-346-0035", website="https://www.childlawwv.org",
        county="Kanawha", served="Kanawha|Putnam|Boone|Clay|Lincoln|Logan", coverage="multi",
        source="https://www.childlawwv.org")

    _mk(add, name="West Virginia Circuit Clerk — Vital Records (Kanawha)", category="id-documentation", region="Charleston / Kanawha County",
        description="Kanawha County Circuit Clerk office issuing certified birth certificates and marriage records needed for DMV ID, WV PATH benefits enrollment, and employment documentation after release.", description_es="Oficina del Secretario del Circuito del condado Kanawha emite certificados de nacimiento y registros matrimoniales necesarios para identificación del DMV, WV PATH y documentación laboral.",
        address="409 Virginia Street East", city="Charleston", phone="304-357-0460", website="https://www.kanawhacounty.org",
        county="Kanawha", served="Kanawha", coverage="single",
        source="https://www.kanawhacounty.org")

    _mk(add, name="West Virginia Circuit Clerk — Vital Records (Cabell)", category="id-documentation", region="Huntington / Cabell County",
        description="Cabell County Circuit Clerk providing certified vital records for residents establishing identity documents after incarceration in the Metro Valley.", description_es="Secretario del Circuito del condado Cabell proporciona registros vitales certificados para residentes que establecen documentos de identidad después de la encarcelación en el valle metropolitano.",
        address="750 5th Avenue", city="Huntington", phone="304-526-8622", website="https://www.cabellcounty.org",
        county="Cabell", served="Cabell", coverage="single",
        source="https://www.cabellcounty.org")

    _mk(add, name="West Virginia Circuit Clerk — Vital Records (Wood)", category="id-documentation", region="Parkersburg / Wood County",
        description="Wood County Circuit Clerk issuing birth certificates and vital records for Mid-Ohio Valley residents obtaining IDs and benefits documentation after release.", description_es="Secretario del Circuito del condado Wood emite certificados de nacimiento y registros vitales para residentes del valle Mid-Ohio obteniendo identificación y documentación de beneficios.",
        address="400 Market Street", city="Parkersburg", phone="304-424-1700", website="https://www.woodcountywv.com",
        county="Wood", served="Wood", coverage="single",
        source="https://www.woodcountywv.com")

    _mk(add, name="West Virginia Circuit Clerk — Vital Records (Berkeley)", category="id-documentation", region="Martinsburg / Berkeley County",
        description="Berkeley County Circuit Clerk providing certified vital records for Eastern Panhandle residents establishing identity for DMV, employment, and WV PATH enrollment.", description_es="Secretario del Circuito del condado Berkeley proporciona registros vitales certificados para residentes del Panhandle Oriental estableciendo identidad para DMV, empleo y WV PATH.",
        address="400 W. Stephen Street", city="Martinsburg", phone="304-264-1926", website="https://www.berkeleycounty.org",
        county="Berkeley", served="Berkeley", coverage="single",
        source="https://www.berkeleycounty.org")

    _mk(add, name="Clothing Closet — Catholic Charities Huntington", category="basic-needs", region="Huntington / Cabell County",
        description="Catholic Charities Huntington clothing closet and emergency assistance for low-income Metro Valley residents including returning citizens needing interview clothing and household basics.", description_es="Despensa de ropa y asistencia de emergencia de Caritas Católica Huntington para residentes de bajos ingresos del valle metropolitano incluidos ciudadanos que regresan necesitando ropa para entrevistas.",
        address="1326 8th Avenue", city="Huntington", phone="304-523-8048", website="https://www.catholiccharitieswv.org",
        county="Cabell", served="Cabell|Wayne|Lincoln", coverage="multi",
        source="https://www.catholiccharitieswv.org")

    _mk(add, name="Mountain Mission — Basic Needs & Thrift", category="basic-needs", region="Charleston / Kanawha County",
        description="Faith-based ministry providing clothing, furniture, household goods, and emergency assistance for low-income Kanawha County families including returning citizens furnishing a first home after release.", description_es="Ministerio basado en la fe con ropa, muebles, artículos del hogar y asistencia de emergencia para familias de bajos ingresos del condado Kanawha incluidos ciudadanos amueblando su primer hogar.",
        address="301 Tennessee Avenue", city="Charleston", phone="304-343-4549", website="https://www.mountainmissionwv.org",
        county="Kanawha", served="Kanawha", coverage="single",
        source="https://www.mountainmissionwv.org")

    _mk(add, name="Christian Help — Emergency Assistance", category="basic-needs", region="Morgantown / Monongalia County",
        description="Morgantown emergency assistance agency providing food pantry, clothing, utility help, and case management for low-income families in Monongalia and Preston counties including returning citizens.", description_es="Agencia de asistencia de emergencia de Morgantown con despensa, ropa, ayuda con servicios y manejo de casos para familias de bajos ingresos en Monongalia y Preston incluidos ciudadanos que regresan.",
        address="219 Walnut Street", city="Morgantown", phone="304-296-0221", website="https://www.christianhelp.org",
        county="Monongalia", served="Monongalia|Preston|Marion", coverage="multi",
        source="https://www.christianhelp.org")

    _mk(add, name="Southern Appalachian Labor School — Youth & Adult Education", category="education", region="Kincaid / Fayette County",
        description="Community-based education and workforce program serving Fayette and Raleigh counties with GED preparation, vocational training, and youth services including justice-involved young adults.", description_es="Programa comunitario de educación y fuerza laboral en Fayette y Raleigh con preparación GED, capacitación vocacional y servicios juveniles incluidos jóvenes adultos con antecedentes penales.",
        address="PO Box 100", city="Kincaid", phone="304-877-2467", website="https://www.sals.info",
        county="Fayette", served="Fayette|Raleigh|Summers|Nicholas", coverage="multi",
        source="https://www.sals.info")

    _mk(add, name="Region 1 Reentry Council — Southern West Virginia", category="reentry-organizations", region="Beckley / Raleigh County",
        description="Regional reentry council connecting southern West Virginia justice-involved residents to local housing, employment, treatment, and benefits partners through REACH Initiative coordination—a navigation council, not a direct-service provider.", description_es="Consejo regional de reinserción conectando residentes con antecedentes penales del sur de WV con aliados locales de vivienda, empleo, tratamiento y beneficios a través de REACH—un consejo de navegación, no proveedor directo.",
        address="200 New River Town Center", city="Beckley", phone="304-256-4444", website="https://www.wvreentry.org",
        county="Raleigh", served="Fayette|Greenbrier|McDowell|Mercer|Monroe|Nicholas|Pocahontas|Raleigh|Summers|Webster|Wyoming", coverage="multi",
        source="https://www.wvreentry.org")

    _mk(add, name="Region 2 Reentry Council — Metro Valley", category="reentry-organizations", region="Huntington / Cabell County",
        description="Metro Valley regional reentry council coordinating partner referrals for justice-involved residents in Cabell, Wayne, and surrounding southwestern counties through the REACH Initiative network.", description_es="Consejo regional de reinserción del valle metropolitano coordinando referencias de aliados para residentes con antecedentes penales en Cabell, Wayne y condados del suroeste a través de REACH.",
        address="2699 Park Avenue", city="Huntington", phone="304-528-5000", website="https://www.wvreentry.org",
        county="Cabell", served="Boone|Cabell|Lincoln|Logan|Mingo|Putnam|Wayne", coverage="multi",
        source="https://www.wvreentry.org")

    _mk(add, name="Region 6 Reentry Council — North Central WV", category="reentry-organizations", region="Fairmont / Marion County",
        description="North-central West Virginia reentry council connecting justice-involved residents in Marion, Harrison, Monongalia, and surrounding counties to local reentry partners through REACH Initiative coordination.", description_es="Consejo de reinserción del centro-norte de WV conectando residentes con antecedentes penales en Marion, Harrison, Monongalia y condados circundantes con aliados locales a través de REACH.",
        address="1900 Kanawha Boulevard East", city="Fairmont", phone="304-368-0416", website="https://www.wvreentry.org",
        county="Marion", served="Barbour|Braxton|Doddridge|Gilmer|Harrison|Lewis|Marion|Monongalia|Preston|Randolph|Taylor|Tucker|Upshur", coverage="multi",
        source="https://www.wvreentry.org")

    _mk(add, name="Region 7 Reentry Council — Eastern Panhandle", category="reentry-organizations", region="Martinsburg / Berkeley County",
        description="Eastern Panhandle reentry council coordinating referrals for justice-involved residents in Berkeley, Jefferson, and eastern counties through the statewide REACH Initiative network.", description_es="Consejo de reinserción del Panhandle Oriental coordinando referencias para residentes con antecedentes penales en Berkeley, Jefferson y condados orientales a través de la red REACH estatal.",
        address="1317 Edwin Miller Boulevard", city="Martinsburg", phone="304-267-0005", website="https://www.wvreentry.org",
        county="Berkeley", served="Berkeley|Grant|Hampshire|Hardy|Jefferson|Mineral|Morgan|Pendleton", coverage="multi",
        source="https://www.wvreentry.org")
