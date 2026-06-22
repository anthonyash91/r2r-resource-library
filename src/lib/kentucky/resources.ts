import type { Resource } from "@/types";
import { KENTUCKY_CATEGORY_BY_ID } from "./categories";

const now = new Date().toISOString();

type ResourceSeed = Omit<
  Resource,
  | "category"
  | "created_at"
  | "updated_at"
  | "view_count"
  | "save_count"
  | "status"
  | "created_by"
  | "is_featured"
> & { is_featured?: boolean };

function buildResource(seed: ResourceSeed): Resource {
  return {
    ...seed,
    category: KENTUCKY_CATEGORY_BY_ID[seed.category_id],
    status: "active",
    is_featured: seed.is_featured ?? false,
    view_count: 0,
    save_count: 0,
    created_at: now,
    updated_at: now,
    created_by: null,
  };
}

const RESOURCE_SEEDS: ResourceSeed[] = [
  {
    id: "res-ky-001",
    name: "Kentucky DOC Division of Reentry Services",
    description:
      "The Kentucky Department of Corrections Division of Reentry Services helps people who are incarcerated or under supervision prepare for successful return to the community. Staff develop individualized reentry plans, connect individuals and families to community resources, and coordinate evidence-based programming focused on life skills, employment readiness, and prosocial behavior. The division partners with local agencies across all 120 counties to address common barriers such as housing, employment, treatment, and transportation. Reentry coordinators are assigned by region to assist with questions about programs, referrals, and community resources before and after release.",
    description_es:
      "La División de Servicios de Reintegración del Departamento de Correcciones de Kentucky ayuda a las personas encarceladas o bajo supervisión a prepararse para un regreso exitoso a la comunidad. El personal elabora planes de reintegración individualizados, conecta a las personas y familias con recursos comunitarios y coordina programas basados en evidencia enfocados en habilidades para la vida, preparación laboral y conducta prosocial. La división colabora con agencias locales en los 120 condados para abordar barreras comunes como vivienda, empleo, tratamiento y transporte. Los coordinadores de reintegración están asignados por región para ayudar con preguntas sobre programas, referidos y recursos comunitarios antes y después de la liberación.",
    category_id: "cat-ky-state-agency",
    state: "Kentucky",
    county: "Franklin",
    city: "Frankfort",
    address: null,
    phone: "502-782-2347",
    website: "https://corrections.ky.gov/Reentry",
    email: null,
    hours: "Monday–Friday, 8 a.m.–4:30 p.m.",
    eligibility:
      "Justice-involved individuals in Kentucky DOC custody or under DOC community supervision, and their families seeking reentry planning support.",
    services: [
      "Individualized reentry planning",
      "Regional reentry coordinator referrals",
      "Community partnership navigation",
      "Pre-release programming coordination",
      "Family support and guidance",
    ],
    tags: ["statewide", "reentry", "DOC", "probation", "parole", "frankfort"],
    is_featured: true,
  },
  {
    id: "res-ky-002",
    name: "Kentucky DOC Reentry Service Centers Program",
    description:
      "The Kentucky Department of Corrections Reentry Service Center (RSC) program, overseen by the Division of Probation and Parole, provides contracted residential reentry for state inmates, parolees, and probationers who are transitioning back to the community. RSCs offer housing, structured programming, vocational training, educational opportunities, cognitive behavioral programming, and substance use treatment at select locations. Participants typically enter near parole eligibility after obtaining community custody status. The program helps individuals reconnect with family, seek employment, and build skills before completing incarceration or supervision.",
    description_es:
      "El programa de Centros de Servicios de Reintegración (RSC) del Departamento de Correcciones de Kentucky, supervisado por la División de Libertad Condicional y Libertad Vigilada, ofrece reintegración residencial contratada para reclusos estatales, personas en libertad condicional y libertad vigilada que regresan a la comunidad. Los RSC ofrecen vivienda, programación estructurada, capacitación vocacional, oportunidades educativas, programación cognitivo-conductual y tratamiento de uso de sustancias en ubicaciones selectas. Los participantes suelen ingresar cerca de la elegibilidad para libertad condicional después de obtener custodia comunitaria. El programa ayuda a reconectarse con la familia, buscar empleo y desarrollar habilidades antes de completar el encarcelamiento o la supervisión.",
    category_id: "cat-ky-probation-parole",
    state: "Kentucky",
    county: null,
    city: null,
    address: null,
    phone: "502-564-7023",
    website: "https://corrections.ky.gov/Facilities/halfway-houses/Pages/reentryservicecenters.aspx",
    email: null,
    hours: "Monday–Friday, 8 a.m.–4:30 p.m.",
    eligibility:
      "Kentucky DOC inmates with community custody status near parole eligibility, and eligible parolees and probationers referred through Probation and Parole.",
    services: [
      "Transitional residential placement",
      "Vocational training",
      "Educational programming",
      "Cognitive behavioral programming",
      "Substance use treatment (select sites)",
      "Employment preparation",
    ],
    tags: ["statewide", "RSC", "probation", "parole", "halfway house", "DOC"],
  },
  {
    id: "res-ky-003",
    name: "Louisville Urban League — Reily Reentry Project",
    description:
      "The Reily Reentry Project at the Louisville Urban League helps justice-involved individuals in Jefferson County remove barriers caused by criminal records. The program facilitates Kentucky expungement for eligible convictions, covers most court and filing fees when approved, and connects participants to holistic Urban League services such as job coaching, health navigation, and financial counseling. Participants complete a needs assessment with a Community Health Navigator and may enroll in additional League programs to support long-term stability. Expungement clinics and record review determine legal eligibility before appointments are scheduled.",
    description_es:
      "El Proyecto Reily de Reintegración de la Liga Urbana de Louisville ayuda a personas con antecedentes de justicia en el condado de Jefferson a eliminar barreras causadas por registros penales. El programa facilita la eliminación de antecedentes de Kentucky para condenas elegibles, cubre la mayoría de las tarifas judiciales y de presentación cuando se aprueba, y conecta a los participantes con servicios integrales de la Liga como orientación laboral, navegación de salud y asesoría financiera. Los participantes completan una evaluación de necesidades con un Navegador de Salud Comunitaria y pueden inscribirse en programas adicionales de la Liga para apoyar la estabilidad a largo plazo. Las clínicas de eliminación de antecedentes y la revisión de registros determinan la elegibilidad legal antes de programar citas.",
    category_id: "cat-ky-legal-aid",
    state: "Kentucky",
    county: "Jefferson",
    city: "Louisville",
    address: "1535 West Broadway",
    phone: "502-585-4622",
    website: "https://lul.org/justice/reily-reentry-project/",
    email: null,
    hours: "Monday–Friday, 9:30 a.m.–4 p.m.",
    eligibility:
      "Individuals with Jefferson County convictions who are legally eligible for expungement under Kentucky law and agree to participate in League support services.",
    services: [
      "Criminal record review",
      "Expungement filing assistance",
      "Court fee assistance",
      "Community Health Navigator assessment",
      "Job coaching referrals",
      "Financial counseling referrals",
    ],
    tags: ["louisville", "jefferson county", "expungement", "legal aid", "reentry"],
    is_featured: true,
  },
  {
    id: "res-ky-004",
    name: "Legal Aid Society — Louisville",
    description:
      "The Legal Aid Society provides free civil legal help to low-income residents of the Louisville region, including criminal record expungement for eligible Kentucky charges. Attorneys and staff assist with expungement petitions, housing issues, public benefits, family matters, and consumer problems that create barriers after release. Intake is required to determine eligibility based on income and legal issue type. Legal Aid does not represent clients in active criminal cases but helps remove civil legal barriers that block employment and housing for justice-involved individuals.",
    description_es:
      "La Sociedad de Asistencia Legal ofrece ayuda legal civil gratuita a residentes de bajos ingresos de la región de Louisville, incluida la eliminación de antecedentes penales para cargos elegibles de Kentucky. Abogados y personal ayudan con peticiones de eliminación de antecedentes, problemas de vivienda, beneficios públicos, asuntos familiares y problemas de consumo que crean barreras después de la liberación. Se requiere admisión para determinar la elegibilidad según ingresos y tipo de problema legal. La Asistencia Legal no representa clientes en casos penales activos, pero ayuda a eliminar barreras legales civiles que bloquean el empleo y la vivienda para personas con antecedentes de justicia.",
    category_id: "cat-ky-legal-aid",
    state: "Kentucky",
    county: "Jefferson",
    city: "Louisville",
    address: "416 W. Muhammad Ali Blvd., Suite 300",
    phone: "502-584-1254",
    website: "https://yourlegalaid.org",
    email: null,
    hours: "Intake Monday–Thursday, 10 a.m.–4 p.m.; office Monday–Friday, 9 a.m.–5 p.m.",
    eligibility:
      "Low-income individuals at or below 125% of the federal poverty guideline in Jefferson, Bullitt, Hardin, Oldham, Shelby, Spencer, and other served counties with civil legal needs including eligible expungements.",
    services: [
      "Criminal record expungement",
      "Housing legal assistance",
      "Public benefits advocacy",
      "Family law assistance",
      "Consumer legal help",
      "Online and phone intake",
    ],
    tags: ["louisville", "jefferson county", "expungement", "legal aid", "civil legal"],
  },
  {
    id: "res-ky-005",
    name: "Legal Aid of the Bluegrass",
    description:
      "Legal Aid of the Bluegrass (LABG) provides free civil legal representation to low-income Kentuckians across Central, Northern, and Eastern Kentucky, including criminal record expungement to remove employment and housing barriers. Staff partner with Goodwill of Kentucky for expungement clinics and help eligible clients file petitions at no cost when they qualify. LABG also assists with housing, public benefits, family safety, and consumer issues. Multiple regional offices serve Fayette, Kenton, Boyd, and surrounding counties through phone intake and online applications.",
    description_es:
      "Legal Aid of the Bluegrass (LABG) brinda representación legal civil gratuita a habitantes de bajos ingresos de Kentucky en las regiones Central, del Norte y del Este, incluida la eliminación de antecedentes penales para quitar barreras de empleo y vivienda. El personal colabora con Goodwill of Kentucky en clínicas de eliminación de antecedentes y ayuda a clientes elegibles a presentar peticiones sin costo cuando califican. LABG también asiste con vivienda, beneficios públicos, seguridad familiar y problemas de consumo. Varias oficinas regionales atienden Fayette, Kenton, Boyd y condados circundantes mediante admisión telefónica y solicitudes en línea.",
    category_id: "cat-ky-legal-aid",
    state: "Kentucky",
    county: "Fayette",
    city: "Lexington",
    address: "300 E. Main Street, Suite 210",
    phone: "859-431-8200",
    website: "https://lablaw.org",
    email: "legalaid@lablaw.org",
    hours: "Office Monday–Friday, 8:30 a.m.–4:30 p.m.; intake Monday–Thursday, 10 a.m.–3 p.m. and Friday, 10 a.m.–1 p.m.",
    eligibility:
      "Low-income individuals in LABG's 33-county service area with civil legal needs, including eligible Kentucky criminal record expungements.",
    services: [
      "Criminal record expungement",
      "Housing legal help",
      "Public benefits assistance",
      "Family law services",
      "Consumer advocacy",
      "Online application intake",
    ],
    tags: ["lexington", "fayette county", "northern kentucky", "eastern kentucky", "expungement", "statewide"],
  },
  {
    id: "res-ky-006",
    name: "Kentucky Career Center — Louisville (KentuckianaWorks)",
    description:
      "The Kentucky Career Center on Broadway, operated through KentuckianaWorks, offers free career services to job seekers in Louisville and Jefferson County, including people recently released from incarceration. Career specialists provide resume help, interview coaching, job search assistance, GED referrals, and connections to training scholarships when available. The center explicitly serves justice-involved job seekers and connects them to quality employers. Services are available at the Goodwill Opportunity Campus and include workshops on LinkedIn, interviewing, and career planning.",
    description_es:
      "El Kentucky Career Center en Broadway, operado a través de KentuckianaWorks, ofrece servicios profesionales gratuitos a quienes buscan empleo en Louisville y el condado de Jefferson, incluidas personas recién liberadas del encarcelamiento. Los especialistas en carreras brindan ayuda con currículums, coaching de entrevistas, asistencia en búsqueda de empleo, referidos de GED y conexiones a becas de capacitación cuando están disponibles. El centro atiende explícitamente a quienes buscan empleo con antecedentes de justicia y los conecta con empleadores de calidad. Los servicios están disponibles en el Goodwill Opportunity Campus e incluyen talleres sobre LinkedIn, entrevistas y planificación de carrera.",
    category_id: "cat-ky-employment",
    state: "Kentucky",
    county: "Jefferson",
    city: "Louisville",
    address: "2820 W Broadway, Suite 100",
    phone: "502-388-3010",
    website: "https://www.kentuckianaworks.org/kcclou",
    email: null,
    hours: "Monday–Friday, 8:30 a.m.–5 p.m.",
    eligibility:
      "Open to all job seekers in the Louisville/Jefferson County area, including justice-involved individuals seeking employment and training support.",
    services: [
      "Resume and cover letter help",
      "Interview coaching",
      "Job search assistance",
      "Career planning workshops",
      "GED referrals",
      "Training scholarship information",
      "Employer connections",
    ],
    tags: ["louisville", "jefferson county", "employment", "second chance", "career center"],
    is_featured: true,
  },
  {
    id: "res-ky-007",
    name: "Kentucky Career Center — Northern Kentucky",
    description:
      "The Kentucky Career Center in Covington connects Northern Kentucky job seekers—including individuals in recovery and those with criminal records—to career coaching, job training, paid internships, and placement assistance. The center hosts partner organizations onsite such as Brighton Center, Gateway Community and Technical College, and Northern Kentucky Community Action Commission. Specialists offer resume building, mock interviews, and referrals to wrap-around supports including transportation and childcare. Reentry-focused career services are highlighted in regional recovery and workforce materials.",
    description_es:
      "El Kentucky Career Center en Covington conecta a quienes buscan empleo en el Norte de Kentucky—incluidas personas en recuperación y con antecedentes penales—con orientación profesional, capacitación laboral, pasantías pagadas y asistencia de colocación. El centro alberga organizaciones asociadas como Brighton Center, Gateway Community and Technical College y Northern Kentucky Community Action Commission. Los especialistas ofrecen elaboración de currículums, entrevistas simuladas y referidos a apoyos integrales incluyendo transporte y cuidado infantil. Los servicios de carrera enfocados en reintegración se destacan en materiales regionales de recuperación y fuerza laboral.",
    category_id: "cat-ky-employment",
    state: "Kentucky",
    county: "Kenton",
    city: "Covington",
    address: "1324 Madison Avenue",
    phone: "859-292-6666",
    website: "https://www.nkcareercenter.org",
    email: null,
    hours: "Monday–Friday, 8 a.m.–4:30 p.m.",
    eligibility:
      "Job seekers in Northern Kentucky, including individuals in reentry and recovery seeking employment and training services.",
    services: [
      "Career coaching",
      "Job training referrals",
      "Paid internships",
      "Job placement assistance",
      "Resume and interview support",
      "Partner agency referrals",
      "Hiring events and job fairs",
    ],
    tags: ["northern kentucky", "covington", "kenton county", "employment", "reentry", "recovery"],
  },
  {
    id: "res-ky-008",
    name: "Center for Employment Opportunities — Louisville",
    description:
      "The Center for Employment Opportunities (CEO) Louisville provides immediate, comprehensive employment services exclusively for people who have recently been released from incarceration. CEO offers paid transitional work experience, job coaching, placement with fair-chance employers, and retention support to reduce recidivism. The Louisville office partners with Kentucky DOC and local employers to connect participants to stable jobs quickly after release. CEO is a national evidence-based reentry employment provider with a dedicated Louisville location serving the metro area.",
    description_es:
      "Center for Employment Opportunities (CEO) Louisville ofrece servicios de empleo inmediatos e integrales exclusivamente para personas recién liberadas del encarcelamiento. CEO ofrece experiencia laboral transicional remunerada, orientación laboral, colocación con empleadores de segunda oportunidad y apoyo de retención para reducir la reincidencia. La oficina de Louisville colabora con el DOC de Kentucky y empleadores locales para conectar a los participantes con empleos estables rápidamente después de la liberación. CEO es un proveedor nacional de empleo de reintegración basado en evidencia con una ubicación dedicada en Louisville que sirve al área metropolitana.",
    category_id: "cat-ky-employment",
    state: "Kentucky",
    county: "Jefferson",
    city: "Louisville",
    address: "321 Guthrie Street",
    phone: "502-694-7878",
    website: "https://www.ceoworks.org/locations/louisville",
    email: null,
    hours: "Monday–Friday, 8 a.m.–5 p.m.",
    eligibility:
      "Adults who have been released from incarceration within the past year (or meet CEO enrollment criteria) and live in the Louisville service area.",
    services: [
      "Paid transitional work",
      "Job placement",
      "Career coaching",
      "Retention support",
      "Employer partnerships",
      "Life skills support",
    ],
    tags: ["louisville", "jefferson county", "employment", "reentry", "CEO", "second chance"],
    is_featured: true,
  },
  {
    id: "res-ky-009",
    name: "Goodwill Kentucky — RISE Program (Lexington)",
    description:
      "Goodwill of Kentucky's RISE (Reintegrating Individuals Successfully Every Day) program provides employment services tailored to justice-involved job seekers in Lexington and Fayette County. Career coaches help participants overcome barriers to work, connect to training and employer partners, and build stability after release. RISE expanded from Louisville to Lexington, Bowling Green, and Pikeville to serve more Kentuckians with criminal backgrounds. The Lexington RISE team can be reached directly for enrollment and referrals.",
    description_es:
      "El programa RISE (Reintegrating Individuals Successfully Every Day) de Goodwill of Kentucky ofrece servicios de empleo adaptados a quienes buscan trabajo con antecedentes de justicia en Lexington y el condado de Fayette. Los coaches de carrera ayudan a los participantes a superar barreras laborales, conectarse con capacitación y empleadores asociados, y construir estabilidad después de la liberación. RISE se expandió de Louisville a Lexington, Bowling Green y Pikeville para atender a más habitantes de Kentucky con antecedentes penales. El equipo RISE de Lexington puede contactarse directamente para inscripción y referidos.",
    category_id: "cat-ky-employment",
    state: "Kentucky",
    county: "Fayette",
    city: "Lexington",
    address: "130 West New Circle Rd., Suite 110",
    phone: "859-806-7956",
    website: "https://goodwillky.org/rise-program-now-offering-services-in-lexington-bowling-green-pikeville/",
    email: null,
    hours: "Monday–Friday, 8 a.m.–4:30 p.m.",
    eligibility:
      "Justice-involved individuals in the Lexington/Fayette County area seeking employment support through Goodwill Kentucky.",
    services: [
      "Employment coaching",
      "Job placement assistance",
      "Barrier removal support",
      "Training referrals",
      "Employer partner connections",
    ],
    tags: ["lexington", "fayette county", "employment", "RISE", "goodwill", "second chance"],
  },
  {
    id: "res-ky-010",
    name: "Goodwill Kentucky — LifeLaunch: Ignite 2.0 (Lexington)",
    description:
      "Goodwill LifeLaunch: Ignite 2.0 is a reentry program for young adults ages 18–24 in Fayette County with current or prior justice involvement. Participants work with career coaches on a personalized pathway that includes job readiness training, enrollment in career credentials through Bluegrass Community and Technical College, and paid work experience with employer partners. The program addresses barriers such as transportation, housing, food insecurity, substance use, and mental health while promoting education and employment to reduce recidivism.",
    description_es:
      "Goodwill LifeLaunch: Ignite 2.0 es un programa de reintegración para jóvenes de 18 a 24 años en el condado de Fayette con participación actual o previa en el sistema de justicia. Los participantes trabajan con coaches de carrera en una ruta personalizada que incluye capacitación de preparación laboral, inscripción en credenciales profesionales a través de Bluegrass Community and Technical College y experiencia laboral remunerada con empleadores asociados. El programa aborda barreras como transporte, vivienda, inseguridad alimentaria, uso de sustancias y salud mental mientras promueve la educación y el empleo para reducir la reincidencia.",
    category_id: "cat-ky-education",
    state: "Kentucky",
    county: "Fayette",
    city: "Lexington",
    address: "130 West New Circle Rd., Suite 110",
    phone: "859-277-3661",
    website: "https://goodwillky.org/ignitelex/",
    email: null,
    hours: "Monday–Friday, 8 a.m.–4:30 p.m.",
    eligibility:
      "Young adults ages 18–24 in Fayette County with prior or current justice involvement willing to enroll in training and work pathways.",
    services: [
      "Career coaching",
      "Job readiness training",
      "BCTC credential pathways",
      "Work and learn placements",
      "Barrier reduction support",
      "Online referral intake",
    ],
    tags: ["lexington", "fayette county", "young adults", "education", "employment", "reentry"],
  },
  {
    id: "res-ky-011",
    name: "Dismas Charities — Louisville Reentry Center",
    description:
      "Dismas Charities operates a residential reentry center in Louisville for men and women transitioning from incarceration back into the community. As a Kentucky DOC-contracted Reentry Service Center provider, Dismas offers structured housing, case management, education, employment support, and family reunification services. The organization has served justice-involved individuals since 1964 with a mission of healing and community reintegration. Programming prepares residents for employment and stable community living before and during community supervision.",
    description_es:
      "Dismas Charities opera un centro de reintegración residencial en Louisville para hombres y mujeres que hacen la transición del encarcelamiento de regreso a la comunidad. Como proveedor contratado del DOC de Kentucky de Centros de Servicios de Reintegración, Dismas ofrece vivienda estructurada, gestión de casos, educación, apoyo laboral y servicios de reunificación familiar. La organización ha servido a personas con antecedentes de justicia desde 1964 con la misión de sanación y reintegración comunitaria. La programación prepara a los residentes para el empleo y una vida comunitaria estable antes y durante la supervisión comunitaria.",
    category_id: "cat-ky-housing",
    state: "Kentucky",
    county: "Jefferson",
    city: "Louisville",
    address: "124 West Oak Street",
    phone: "502-634-3608",
    website: "https://www.dismas.com",
    email: null,
    hours: "Contact facility for visiting and admission hours",
    eligibility:
      "Kentucky DOC inmates, parolees, and probationers referred to a Reentry Service Center through the Department of Corrections.",
    services: [
      "Transitional housing",
      "Case management",
      "Education programs",
      "Employment support",
      "Family reunification",
      "Life skills programming",
    ],
    tags: ["louisville", "jefferson county", "RSC", "housing", "reentry", "DOC"],
  },
  {
    id: "res-ky-012",
    name: "Life Learning Center",
    description:
      "Life Learning Center in Covington is a nonprofit reentry and workforce program serving Northern Kentucky, including Kenton County Detention Center partners and justice-involved adults. Their transformational change model provides life skills education, career preparation, recovery supports, and basic essentials for people released from jail with felony or misdemeanor histories. Approximately 93% of participants have criminal convictions. Graduates receive help securing employment, and the center hosts regional reentry resource events with dozens of community partners.",
    description_es:
      "Life Learning Center en Covington es un programa sin fines de lucro de reintegración y fuerza laboral que sirve al Norte de Kentucky, incluidos socios del Centro de Detención del condado de Kenton y adultos con antecedentes de justicia. Su modelo de cambio transformacional ofrece educación en habilidades para la vida, preparación profesional, apoyos de recuperación y artículos básicos para personas liberadas de la cárcel con antecedentes penales por delitos graves o menores. Aproximadamente el 93% de los participantes tienen condenas penales. Los graduados reciben ayuda para conseguir empleo, y el centro organiza eventos regionales de recursos de reintegración con docenas de socios comunitarios.",
    category_id: "cat-ky-reentry-orgs",
    state: "Kentucky",
    county: "Kenton",
    city: "Covington",
    address: "20 West 18th Street",
    phone: "859-431-0100",
    website: "https://www.lifelearningcenter.us",
    email: "info@lifelearningcenter.us",
    hours: "Monday–Friday, 8 a.m.–5 p.m.",
    eligibility:
      "At-risk and justice-involved adults in Northern Kentucky seeking life skills, career training, and reentry support; program application required.",
    services: [
      "Life skills curriculum",
      "Career preparation",
      "Recovery support coordination",
      "Release essentials and clothing",
      "Employment placement help",
      "Reentry resource events",
    ],
    tags: ["northern kentucky", "covington", "kenton county", "reentry", "workforce", "recovery"],
    is_featured: true,
  },
  {
    id: "res-ky-013",
    name: "Lexington Second Chance Academy",
    description:
      "The Second Chance Academy is a workforce reentry program led by Lexington-Fayette Urban County Government Economic Development in partnership with the Fayette County Detention Center and Jubilee Jobs of Lexington. It serves individuals with six months or less remaining on their sentence through a structured seven-week course focused on life and job skills. After release, participants receive at least one year of individualized support to find and keep employment and successfully transition back into the community.",
    description_es:
      "La Second Chance Academy es un programa de reintegración laboral liderado por el Desarrollo Económico del Gobierno Urbano del Condado Lexington-Fayette en asociación con el Centro de Detención del condado de Fayette y Jubilee Jobs of Lexington. Atiende a personas con seis meses o menos restantes de condena mediante un curso estructurado de siete semanas enfocado en habilidades para la vida y el trabajo. Después de la liberación, los participantes reciben al menos un año de apoyo individualizado para encontrar y mantener empleo y hacer la transición exitosamente de regreso a la comunidad.",
    category_id: "cat-ky-education",
    state: "Kentucky",
    county: "Fayette",
    city: "Lexington",
    address: "200 E. Main St.",
    phone: "859-258-3100",
    website: "https://www.lexingtonky.gov/economic-development/second-chance-academy",
    email: "katkins@lexingtonky.gov",
    hours: "Monday–Friday, 8 a.m.–5 p.m.",
    eligibility:
      "Individuals incarcerated at Fayette County Detention Center with approximately six months or less remaining on their sentence, selected through program partnership.",
    services: [
      "Seven-week reentry course",
      "Life skills training",
      "Job readiness training",
      "Post-release case support (1+ year)",
      "Employment retention assistance",
    ],
    tags: ["lexington", "fayette county", "second chance", "workforce", "jail reentry"],
  },
  {
    id: "res-ky-014",
    name: "Lexington Rescue Mission — Ex-Offender Re-Entry",
    description:
      "Lexington Rescue Mission provides faith-based reentry support for incarcerated and recently released men and women in Central Kentucky. Inside local jails—including Fayette, Woodford, and Madison County detention centers—the Mission offers Genesis Process and Jobs for Life classes. After release, a reentry case manager helps develop transition plans and assists with IDs, transportation, clothing, housing, and employment. Volunteer mentors provide ongoing support, and family support is available through Bluegrass Families of the Incarcerated.",
    description_es:
      "Lexington Rescue Mission brinda apoyo de reintegración basado en la fe para hombres y mujeres encarcelados y recién liberados en el centro de Kentucky. Dentro de las cárceles locales—incluidos los centros de detención de los condados de Fayette, Woodford y Madison—la Misión ofrece clases Genesis Process y Jobs for Life. Después de la liberación, un gestor de casos de reintegración ayuda a desarrollar planes de transición y asiste con identificaciones, transporte, ropa, vivienda y empleo. Mentores voluntarios brindan apoyo continuo, y el apoyo familiar está disponible a través de Bluegrass Families of the Incarcerated.",
    category_id: "cat-ky-reentry-orgs",
    state: "Kentucky",
    county: "Fayette",
    city: "Lexington",
    address: null,
    phone: "859-785-0979",
    website: "https://lexingtonrescue.org/services/ex-offender-re-entry/",
    email: null,
    hours: "Contact program staff for appointment times",
    eligibility:
      "Incarcerated and recently released individuals participating in Mission jail classes or referred for reentry case management in the Lexington region.",
    services: [
      "In-jail reentry classes",
      "Jobs for Life training",
      "Genesis Process classes",
      "Reentry case management",
      "ID and document assistance",
      "Housing and employment referrals",
      "Family support groups",
    ],
    tags: ["lexington", "fayette county", "madison county", "woodford county", "reentry", "faith-based"],
  },
  {
    id: "res-ky-015",
    name: "Hope Center — SHARE Reentry Program",
    description:
      "The Hope Center SHARE (Supportive Housing for Adaptive ReEntry) program in Lexington provides long-term residential recovery services for Kentucky DOC-referred individuals with substance use disorders and serious mental illness. SHARE operates separate tracks for co-occurring disorders and serious mental illness, with male services at Jacob's House and female services at the Ball-Quantrell Jones Center for Women. Clinical programming combines housing, behavioral health treatment, and peer support to prepare participants for community reintegration.",
    description_es:
      "El programa SHARE (Supportive Housing for Adaptive ReEntry) del Hope Center en Lexington ofrece servicios residenciales de recuperación a largo plazo para personas referidas por el DOC de Kentucky con trastornos por uso de sustancias y enfermedades mentales graves. SHARE opera rutas separadas para trastornos coexistentes y enfermedad mental grave, con servicios para hombres en Jacob's House y servicios para mujeres en el Ball-Quantrell Jones Center for Women. La programación clínica combina vivienda, tratamiento de salud conductual y apoyo entre pares para preparar a los participantes para la reintegración comunitaria.",
    category_id: "cat-ky-substance-use",
    state: "Kentucky",
    county: "Fayette",
    city: "Lexington",
    address: "289 West Loudon Avenue",
    phone: "859-543-2222",
    website: "https://hopectr.org/what-we-do/mental-health/",
    email: "sluchetefeld@hopectr.org",
    hours: "Contact program for admission hours",
    eligibility:
      "Kentucky DOC-referred individuals with substance use disorder and/or serious mental illness who meet clinical screening for SHARE programming.",
    services: [
      "Long-term residential recovery",
      "Co-occurring disorder treatment",
      "Serious mental illness support",
      "Peer mentorship",
      "Clinical case management",
      "DOC partnership programming",
    ],
    tags: ["lexington", "fayette county", "SUD", "mental health", "RSC", "recovery housing"],
  },
  {
    id: "res-ky-016",
    name: "Men's Addiction Recovery Center (Recovery Kentucky)",
    description:
      "The Men's Addiction Recovery Center (M.A.R.C.) in Bowling Green is a Kentucky Recovery Kentucky Center contracted through the Department of Corrections to provide peer-driven substance use disorder treatment and housing for justice-involved men. The Recovery Kentucky model uses phased programming based on 12-step principles and recovery dynamics to address addiction and homelessness. The program serves DOC clients needing residential treatment and can connect graduates to longer-term recovery and housing supports in the Bowling Green region.",
    description_es:
      "El Men's Addiction Recovery Center (M.A.R.C.) en Bowling Green es un Centro Recovery Kentucky contratado a través del Departamento de Correcciones para brindar tratamiento de trastornos por uso de sustancias impulsado por pares y vivienda para hombres con antecedentes de justicia. El modelo Recovery Kentucky utiliza programación por fases basada en principios de 12 pasos y dinámicas de recuperación para abordar la adicción y la falta de vivienda. El programa atiende a clientes del DOC que necesitan tratamiento residencial y puede conectar a graduados con apoyos de recuperación y vivienda a largo plazo en la región de Bowling Green.",
    category_id: "cat-ky-substance-use",
    state: "Kentucky",
    county: "Warren",
    city: "Bowling Green",
    address: "1791 River Street",
    phone: "270-715-0810",
    website: "https://corrections.ky.gov/Facilities/halfway-houses/Pages/recoverykentucky.aspx",
    email: null,
    hours: "Contact facility for program hours",
    eligibility:
      "Kentucky DOC clients with substance use disorder requiring residential treatment who are approved through DOC Addiction Services clinical assessment.",
    services: [
      "Residential SUD treatment",
      "Peer-driven recovery phases",
      "12-step based programming",
      "Recovery housing",
      "Life skills development",
      "DOC program credit upon completion",
    ],
    tags: ["bowling green", "warren county", "recovery kentucky", "SUD", "DOC", "western kentucky"],
  },
  {
    id: "res-ky-017",
    name: "Northern Kentucky Addiction Helpline",
    description:
      "The Northern Kentucky Addiction Helpline, operated through the Northern Kentucky Office of Drug Control Policy, connects individuals and families to substance use treatment, recovery supports, and reentry resources 24 hours a day. Trained care coordinators answer calls and help with assessment, treatment placement, Casey’s Law support, harm reduction, and linkage to recovery and reentry services across Boone, Kenton, Campbell, and surrounding counties. The helpline is a starting point for justice-involved individuals seeking SUD treatment after jail or prison.",
    description_es:
      "La Línea de Ayuda de Adicciones del Norte de Kentucky, operada a través de la Oficina de Control de Drogas del Norte de Kentucky, conecta a individuos y familias con tratamiento de uso de sustancias, apoyos de recuperación y recursos de reintegración las 24 horas del día. Coordinadores de atención capacitados responden llamadas y ayudan con evaluación, colocación en tratamiento, apoyo de la Ley Casey, reducción de daños y enlace a servicios de recuperación y reintegración en los condados de Boone, Kenton, Campbell y circundantes. La línea de ayuda es un punto de partida para personas con antecedentes de justicia que buscan tratamiento de TUS después de la cárcel o prisión.",
    category_id: "cat-ky-healthcare",
    state: "Kentucky",
    county: "Kenton",
    city: "Covington",
    address: null,
    phone: "859-415-9280",
    website: "https://nkyodcp.org/nky-helpline/",
    email: null,
    hours: "24 hours a day, 7 days a week",
    eligibility:
      "Anyone in Northern Kentucky seeking substance use treatment, recovery support, or reentry linkage, including justice-involved individuals and families.",
    services: [
      "24/7 phone support",
      "Treatment assessment and placement",
      "Recovery service referrals",
      "Reentry resource linkage",
      "Casey's Law support",
      "Harm reduction information",
    ],
    tags: ["northern kentucky", "covington", "SUD", "helpline", "recovery", "reentry"],
  },
  {
    id: "res-ky-018",
    name: "Southern Kentucky Reentry Council",
    description:
      "The Southern Kentucky Reentry Council is a nonprofit coalition serving justice-involved individuals in the Bowling Green region and surrounding counties through the Barren River Area Development District (BRADD). The council helps people leaving jail with transportation, identification, driver's licenses, housing referrals, toiletries, Narcan, and scholarship opportunities. Partnering with local jails and community agencies, SKRC connects newly released individuals to services that reduce recidivism and support stable reintegration in Southern Kentucky.",
    description_es:
      "El Southern Kentucky Reentry Council es una coalición sin fines de lucro que sirve a personas con antecedentes de justicia en la región de Bowling Green y condados circundantes a través del Barren River Area Development District (BRADD). El consejo ayuda a las personas que salen de la cárcel con transporte, identificación, licencias de conducir, referidos de vivienda, artículos de aseo, Narcan y oportunidades de becas. En asociación con cárceles locales y agencias comunitarias, SKRC conecta a personas recién liberadas con servicios que reducen la reincidencia y apoyan una reintegración estable en el sur de Kentucky.",
    category_id: "cat-ky-reentry-orgs",
    state: "Kentucky",
    county: "Warren",
    city: "Bowling Green",
    address: "1945 Scottsville Road, PMB 394",
    phone: null,
    website: "https://southernkyreentry.org",
    email: "info@southernkyreentry.org",
    hours: "Contact by email for assistance",
    eligibility:
      "Justice-involved individuals in Southern Kentucky needing reentry navigation, basic needs, ID help, or referral to local services.",
    services: [
      "Reentry navigation",
      "Transportation assistance",
      "ID and driver's license help",
      "Housing referrals",
      "Release care packages",
      "Narcan distribution",
      "Community scholarships",
    ],
    tags: ["bowling green", "warren county", "southern kentucky", "reentry council", "BRADD"],
  },
  {
    id: "res-ky-019",
    name: "CTS-Russell Reentry Service Center",
    description:
      "CTS-Russell is a Kentucky Department of Corrections-contracted Reentry Service Center in Louisville providing residential reentry programming for eligible state inmates, parolees, and probationers. The facility offers structured housing, cognitive behavioral programming, vocational and educational opportunities, and substance use treatment options to support transition back to the Jefferson County community. RSC participants work toward employment and family reconnection while completing DOC community custody requirements.",
    description_es:
      "CTS-Russell es un Centro de Servicios de Reintegración contratado por el Departamento de Correcciones de Kentucky en Louisville que ofrece programación residencial de reintegración para reclusos estatales elegibles, personas en libertad condicional y libertad vigilada. La instalación ofrece vivienda estructurada, programación cognitivo-conductual, oportunidades vocacionales y educativas, y opciones de tratamiento de uso de sustancias para apoyar la transición de regreso a la comunidad del condado de Jefferson. Los participantes del RSC trabajan hacia el empleo y la reconexión familiar mientras completan los requisitos de custodia comunitaria del DOC.",
    category_id: "cat-ky-housing",
    state: "Kentucky",
    county: "Jefferson",
    city: "Louisville",
    address: "1407 West Jefferson Street",
    phone: "502-855-6500",
    website: "https://corrections.ky.gov/Facilities/halfway-houses/Pages/reentryservicecenters.aspx",
    email: null,
    hours: "Contact facility for program hours",
    eligibility:
      "Kentucky DOC inmates with community custody near parole eligibility and eligible parolees/probationers referred through Probation and Parole.",
    services: [
      "Transitional housing",
      "Cognitive behavioral programming",
      "Vocational training",
      "Educational programs",
      "Substance use treatment",
      "Employment preparation",
    ],
    tags: ["louisville", "jefferson county", "RSC", "housing", "DOC", "reentry"],
  },
  {
    id: "res-ky-020",
    name: "Louisville Metro Department of Corrections — F2ACT Discharge Planning",
    description:
      "Louisville Metro Department of Corrections (LMDC) provides discharge planning and post-release support through its Familiar Faces in Action and Community Treatment (F2ACT) program for vulnerable individuals leaving the Jefferson County jail. F2ACT coordinates clothing, transportation, referrals to shelter or treatment, warm handoffs to community providers, and up to six months of service coordination after release. The program targets people at high risk of cycling between jail and homelessness who need connection to community-based reentry supports.",
    description_es:
      "El Departamento de Correcciones Metro de Louisville (LMDC) proporciona planificación de egreso y apoyo posterior a la liberación a través de su programa Familiar Faces in Action and Community Treatment (F2ACT) para personas vulnerables que salen de la cárcel del condado de Jefferson. F2ACT coordina ropa, transporte, referidos a refugio o tratamiento, traspasos cálidos a proveedores comunitarios y hasta seis meses de coordinación de servicios después de la liberación. El programa se dirige a personas con alto riesgo de alternar entre la cárcel y la falta de vivienda que necesitan conexión con apoyos comunitarios de reintegración.",
    category_id: "cat-ky-basic-needs",
    state: "Kentucky",
    county: "Jefferson",
    city: "Louisville",
    address: "400 S. Sixth Street",
    phone: "502-574-8477",
    website: "https://louisvilleky.gov/government/corrections/correction-cares-programs-and-services",
    email: null,
    hours: "Monday–Friday, 8 a.m.–5 p.m.",
    eligibility:
      "Individuals incarcerated at Louisville Metro Department of Corrections identified as vulnerable and enrolled in F2ACT discharge planning prior to release.",
    services: [
      "Discharge planning",
      "Post-release service coordination (up to 6 months)",
      "Clothing and basic needs",
      "Transportation to placements",
      "Shelter and treatment referrals",
      "Warm handoff to community providers",
    ],
    tags: ["louisville", "jefferson county", "jail reentry", "F2ACT", "discharge planning", "basic needs"],
  },
];

export const KENTUCKY_RESOURCES: Resource[] = RESOURCE_SEEDS.map(buildResource);
