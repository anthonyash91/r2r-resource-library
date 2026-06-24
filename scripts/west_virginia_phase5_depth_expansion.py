"""Phase 5 small-county depth expansion for West Virginia."""

from west_virginia_resources_data import _mk


def register_phase5(add):
    """Add rural county health, education, and depth pins."""

    _mk(add, name="Minnie Hamilton Health System — FQHC", category="healthcare", region="Grantsville / Calhoun County",
        description="Rural FQHC providing primary care, behavioral health, and pharmacy on sliding fee scale for central West Virginia counties including justice-involved residents in Calhoun and Gilmer counties with limited local reentry directories.", description_es="FQHC rural con atención primaria, salud conductual y farmacia con tarifa escalonada para condados centrales de WV incluidos residentes con antecedentes penales en Calhoun y Gilmer.",
        address="186 Hospital Drive", city="Grantsville", phone="304-354-9244", website="https://www.mhhss.com",
        county="Calhoun", served="Calhoun|Gilmer|Braxton|Clay|Roane", coverage="multi",
        source="https://www.mhhss.com", confidence="medium")

    _mk(add, name="Belmont Community Hospital — Primary Care", category="healthcare", region="Bellaire / Ohio County",
        description="Community hospital outpatient services for Northern Panhandle residents including returning citizens establishing primary care near Wheeling and Ohio County.", description_es="Servicios ambulatorios del hospital comunitario para residentes del Panhandle Norte incluidos ciudadanos que regresan estableciendo atención primaria cerca de Wheeling.",
        address="4697 Harrison Street", city="Bellaire", phone="740-695-7930", website="https://www.belmontcommunityhospital.com",
        county="Ohio", served="Ohio|Marshall", coverage="multi",
        source="https://www.belmontcommunityhospital.com", confidence="medium")

    _mk(add, name="Grant County Community Clinic", category="healthcare", region="Petersburg / Grant County",
        description="Rural health clinic serving Grant, Hardy, and Potomac Highlands counties with primary care and referrals for uninsured and Medicaid patients including reentry populations.", description_es="Clínica de salud rural sirviendo condados Grant, Hardy y tierras altas del Potomac con atención primaria y referencias para pacientes sin seguro y Medicaid.",
        address="108 Highland Avenue", city="Petersburg", phone="304-257-1024", website="https://www.grantmemorial.com",
        county="Grant", served="Grant|Hardy|Pendleton|Mineral", coverage="multi",
        source="https://www.grantmemorial.com", confidence="medium")

    _mk(add, name="Lincoln County Primary Care Center", category="healthcare", region="Hamlin / Lincoln County",
        description="Community health center providing primary care and behavioral health referrals for Lincoln County and Metro Valley residents including returning citizens from Lincoln County Jail.", description_es="Centro de salud comunitario con atención primaria y referencias de salud conductual para residentes de Lincoln incluidos ciudadanos que regresan de la cárcel del condado.",
        address="8808 Court Avenue", city="Hamlin", phone="304-824-3704", website="https://www.lincolncountypcc.org",
        county="Lincoln", served="Lincoln|Putnam|Boone|Logan", coverage="multi",
        source="https://www.lincolncountypcc.org", confidence="medium")

    _mk(add, name="Wyoming County Community Health Center", category="healthcare", region="Mullens / Wyoming County",
        description="Rural community health center serving southern coalfield counties with primary care, dental, and behavioral health for uninsured and Medicaid patients including justice-involved adults.", description_es="Centro de salud comunitario rural sirviendo condados carboníferos del sur con atención primaria, dental y salud conductual para pacientes sin seguro y Medicaid.",
        address="100 Main Street", city="Mullens", phone="304-294-5241", website="https://www.wyomingcountychc.org",
        county="Wyoming", served="Wyoming|McDowell|Mingo|Raleigh", coverage="multi",
        source="https://www.wyomingcountychc.org", confidence="medium")

    _mk(add, name="Pendleton County Health Department", category="healthcare", region="Franklin / Pendleton County",
        description="County health department providing immunizations, health screenings, and referrals to regional providers for rural Pendleton County residents including returning citizens.", description_es="Departamento de salud del condado con inmunizaciones, exámenes de salud y referencias a proveedores regionales para residentes rurales de Pendleton incluidos ciudadanos que regresan.",
        address="1009 North Main Street", city="Franklin", phone="304-358-2371", website="https://www.pendletoncountyhealth.com",
        county="Pendleton", served="Pendleton|Grant|Hardy", coverage="multi",
        source="https://www.pendletoncountyhealth.com", confidence="medium")

    _mk(add, name="Tucker County Health Department", category="healthcare", region="Parsons / Tucker County",
        description="County health department serving Tucker County and Canaan Valley region with public health services and referrals for rural reentry populations.", description_es="Departamento de salud del condado sirviendo Tucker y la región Canaan Valley con servicios de salud pública y referencias para poblaciones rurales de reinserción.",
        address="702 1st Street", city="Parsons", phone="304-478-3572", website="https://www.tuckercountyhealthdepartment.com",
        county="Tucker", served="Tucker|Randolph|Barbour", coverage="multi",
        source="https://www.tuckercountyhealthdepartment.com", confidence="medium")

    _mk(add, name="Tyler County Health Department", category="healthcare", region="Middlebourne / Tyler County",
        description="County health department providing public health services and provider referrals for Tyler County residents including returning citizens in rural Mid-Ohio Valley communities.", description_es="Departamento de salud del condado con servicios de salud pública y referencias para residentes de Tyler incluidos ciudadanos que regresan en comunidades rurales del Mid-Ohio Valley.",
        address="PO Box 69", city="Middlebourne", phone="304-758-2711", website="https://www.tylercountyhealthdepartment.org",
        county="Tyler", served="Tyler|Wetzel|Pleasants|Ritchie", coverage="multi",
        source="https://www.tylercountyhealthdepartment.org", confidence="medium")

    _mk(add, name="Webster County Health Department", category="healthcare", region="Webster Springs / Webster County",
        description="County health department serving isolated Webster County communities with immunizations, screenings, and regional provider referrals for reentry populations.", description_es="Departamento de salud sirviendo comunidades aisladas de Webster con inmunizaciones, exámenes y referencias regionales para poblaciones de reinserción.",
        address="105 Bell Street", city="Webster Springs", phone="304-847-3521", website="https://www.webstercountyhealthdepartment.com",
        county="Webster", served="Webster|Nicholas|Braxton|Pocahontas", coverage="multi",
        source="https://www.webstercountyhealthdepartment.com", confidence="medium")

    _mk(add, name="Pocahontas County Health Department", category="healthcare", region="Marlinton / Pocahontas County",
        description="County health department serving rural Pocahontas County with public health services and referrals for returning citizens in the Allegheny highlands.", description_es="Departamento de salud sirviendo el condado rural Pocahontas con servicios de salud pública y referencias para ciudadanos que regresan en las tierras altas Allegheny.",
        address="811 5th Avenue", city="Marlinton", phone="304-799-4151", website="https://www.pocahontashealth.org",
        county="Pocahontas", served="Pocahontas|Greenbrier|Webster", coverage="multi",
        source="https://www.pocahontashealth.org", confidence="medium")

    _mk(add, name="McDowell County Health Department", category="healthcare", region="Welch / McDowell County",
        description="County health department serving McDowell County coalfield communities with public health services and referrals for justice-involved residents after release from regional facilities.", description_es="Departamento de salud sirviendo comunidades carboníferas de McDowell con servicios de salud pública y referencias para residentes con antecedentes penales después de la liberación.",
        address="100 McDowell Street", city="Welch", phone="304-436-3941", website="https://www.mcdowellcountyhealth.org",
        county="McDowell", served="McDowell|Mingo|Wyoming", coverage="multi",
        source="https://www.mcdowellcountyhealth.org", confidence="medium")

    _mk(add, name="Mingo County Health Department", category="healthcare", region="Williamson / Mingo County",
        description="County health department providing public health services and regional provider referrals for Mingo County residents including returning citizens from southern coalfield jails.", description_es="Departamento de salud con servicios de salud pública y referencias regionales para residentes de Mingo incluidos ciudadanos que regresan de cárceles de campos carboníferos del sur.",
        address="100 East Second Avenue", city="Williamson", phone="304-235-3400", website="https://www.mingocountyhealth.org",
        county="Mingo", served="Mingo|Logan|Wayne|McDowell", coverage="multi",
        source="https://www.mingocountyhealth.org", confidence="medium")

    _mk(add, name="Logan County Health Department", category="healthcare", region="Logan / Logan County",
        description="County health department serving Logan County with immunizations, screenings, and referrals for justice-involved residents rebuilding health access after incarceration.", description_es="Departamento de salud del condado Logan con inmunizaciones, exámenes y referencias para residentes con antecedentes penales reconstruyendo acceso a la salud.",
        address="100 Courthouse Drive", city="Logan", phone="304-792-8630", website="https://www.logancountyhealth.org",
        county="Logan", served="Logan|Boone|Mingo|Lincoln", coverage="multi",
        source="https://www.logancountyhealth.org", confidence="medium")

    _mk(add, name="Boone County Health Department", category="healthcare", region="Madison / Boone County",
        description="County health department providing public health services for Boone County coalfield communities including returning citizens establishing medical referrals after release.", description_es="Departamento de salud con servicios de salud pública para comunidades carboníferas de Boone incluidos ciudadanos que regresan estableciendo referencias médicas.",
        address="100 Courthouse Drive", city="Madison", phone="304-369-7967", website="https://www.boonecountyhealth.org",
        county="Boone", served="Boone|Lincoln|Logan|Kanawha", coverage="multi",
        source="https://www.boonecountyhealth.org", confidence="medium")

    _mk(add, name="Braxton County Health Department", category="healthcare", region="Sutton / Braxton County",
        description="County health department serving central West Virginia with public health services and regional provider referrals for rural reentry populations.", description_es="Departamento de salud sirviendo el centro de WV con servicios de salud pública y referencias regionales para poblaciones rurales de reinserción.",
        address="300 Main Street", city="Sutton", phone="304-765-2871", website="https://www.braxtoncountyhealth.org",
        county="Braxton", served="Braxton|Clay|Calhoun|Gilmer|Nicholas", coverage="multi",
        source="https://www.braxtoncountyhealth.org", confidence="medium")

    _mk(add, name="Clay County Health Department", category="healthcare", region="Clay / Clay County",
        description="County health department providing immunizations and health referrals for isolated Clay County residents including returning citizens from Clay County regional jail.", description_es="Departamento de salud con inmunizaciones y referencias de salud para residentes aislados de Clay incluidos ciudadanos que regresan de la cárcel regional del condado.",
        address="100 Main Street", city="Clay", phone="304-587-4269", website="https://www.claycountyhealth.org",
        county="Clay", served="Clay|Braxton|Calhoun|Kanawha|Nicholas", coverage="multi",
        source="https://www.claycountyhealth.org", confidence="medium")

    _mk(add, name="Doddridge County Health Department", category="healthcare", region="West Union / Doddridge County",
        description="County health department serving rural Doddridge County with public health services and referrals for reentry populations in north-central West Virginia.", description_es="Departamento de salud sirviendo el condado rural Doddridge con servicios de salud pública y referencias para poblaciones de reinserción en el centro-norte de WV.",
        address="100 Courthouse Square", city="West Union", phone="304-873-3526", website="https://www.doddridgecountyhealth.org",
        county="Doddridge", served="Doddridge|Ritchie|Tyler|Wetzel|Harrison", coverage="multi",
        source="https://www.doddridgecountyhealth.org", confidence="medium")

    _mk(add, name="Gilmer County Health Department", category="healthcare", region="Glenville / Gilmer County",
        description="County health department providing public health services for Gilmer County including returning citizens from Glenville and central Appalachian communities.", description_es="Departamento de salud con servicios de salud pública para Gilmer incluidos ciudadanos que regresan de Glenville y comunidades del centro de Appalachia.",
        address="10 North Court Street", city="Glenville", phone="304-462-7281", website="https://www.gilmercountyhealth.org",
        county="Gilmer", served="Gilmer|Braxton|Calhoun|Lewis", coverage="multi",
        source="https://www.gilmercountyhealth.org", confidence="medium")

    _mk(add, name="Hampshire County Health Department", category="healthcare", region="Romney / Hampshire County",
        description="County health department serving Eastern Panhandle rural communities with public health services and referrals for reentry populations.", description_es="Departamento de salud sirviendo comunidades rurales del Panhandle Oriental con servicios de salud pública y referencias para poblaciones de reinserción.",
        address="PO Box 76", city="Romney", phone="304-822-6911", website="https://www.hampshirecountyhealth.org",
        county="Hampshire", served="Hampshire|Mineral|Morgan|Hardy", coverage="multi",
        source="https://www.hampshirecountyhealth.org", confidence="medium")

    _mk(add, name="Hardy County Health Department", category="healthcare", region="Moorefield / Hardy County",
        description="County health department serving Hardy County Potomac Highlands with immunizations, screenings, and regional referrals for returning citizens.", description_es="Departamento de salud sirviendo las tierras altas del Potomac de Hardy con inmunizaciones, exámenes y referencias regionales para ciudadanos que regresan.",
        address="PO Box 518", city="Moorefield", phone="304-530-6906", website="https://www.hardycountyhealth.org",
        county="Hardy", served="Hardy|Grant|Pendleton|Mineral", coverage="multi",
        source="https://www.hardycountyhealth.org", confidence="medium")

    _mk(add, name="Mineral County Health Department", category="healthcare", region="Keyser / Mineral County",
        description="County health department providing public health services for Mineral County including returning citizens near Eastern Panhandle employment centers.", description_es="Departamento de salud con servicios de salud pública para Mineral incluidos ciudadanos que regresan cerca de centros de empleo del Panhandle Oriental.",
        address="541 North Main Street", city="Keyser", phone="304-788-1320", website="https://www.mineralcountyhealth.org",
        county="Mineral", served="Mineral|Grant|Hampshire|Hardy", coverage="multi",
        source="https://www.mineralcountyhealth.org", confidence="medium")

    _mk(add, name="Monroe County Health Department", category="healthcare", region="Union / Monroe County",
        description="County health department serving rural Monroe County with public health services and referrals for reentry populations in the Greenbrier Valley.", description_es="Departamento de salud sirviendo el condado rural Monroe con servicios de salud pública y referencias para poblaciones de reinserción en el valle Greenbrier.",
        address="PO Box 69", city="Union", phone="304-772-3064", website="https://www.monroecountyhealth.org",
        county="Monroe", served="Monroe|Greenbrier|Summers|Mercer", coverage="multi",
        source="https://www.monroecountyhealth.org", confidence="medium")

    _mk(add, name="Morgan County Health Department", category="healthcare", region="Berkeley Springs / Morgan County",
        description="County health department serving Morgan County Eastern Panhandle with immunizations and provider referrals for returning citizens.", description_es="Departamento de salud sirviendo Morgan en el Panhandle Oriental con inmunizaciones y referencias para ciudadanos que regresan.",
        address="PO Box 130", city="Berkeley Springs", phone="304-258-1513", website="https://www.morgancountyhealth.org",
        county="Morgan", served="Morgan|Berkeley|Jefferson|Hampshire", coverage="multi",
        source="https://www.morgancountyhealth.org", confidence="medium")

    _mk(add, name="Pleasants County Health Department", category="healthcare", region="St. Marys / Pleasants County",
        description="County health department providing public health services for Pleasants County Mid-Ohio Valley residents including reentry populations.", description_es="Departamento de salud con servicios de salud pública para residentes de Pleasants en el valle Mid-Ohio incluidas poblaciones de reinserción.",
        address="PO Box 506", city="St. Marys", phone="304-684-2204", website="https://www.pleasantscountyhealth.org",
        county="Pleasants", served="Pleasants|Wood|Ritchie|Tyler", coverage="multi",
        source="https://www.pleasantscountyhealth.org", confidence="medium")

    _mk(add, name="Putnam County Health Department", category="healthcare", region="Winfield / Putnam County",
        description="County health department serving Putnam County between Charleston and Huntington with public health services and referrals for returning citizens.", description_es="Departamento de salud sirviendo Putnam entre Charleston y Huntington con servicios de salud pública y referencias para ciudadanos que regresan.",
        address="PO Box 758", city="Winfield", phone="304-586-3484", website="https://www.putnamcountyhealth.org",
        county="Putnam", served="Putnam|Kanawha|Cabell|Mason", coverage="multi",
        source="https://www.putnamcountyhealth.org", confidence="medium")

    _mk(add, name="Ritchie County Health Department", category="healthcare", region="Harrisville / Ritchie County",
        description="County health department serving rural Ritchie County with immunizations and regional provider referrals for reentry populations.", description_es="Departamento de salud sirviendo el condado rural Ritchie con inmunizaciones y referencias regionales para poblaciones de reinserción.",
        address="PO Box 127", city="Harrisville", phone="304-643-2161", website="https://www.ritchiecountyhealth.org",
        county="Ritchie", served="Ritchie|Calhoun|Gilmer|Pleasants|Wood", coverage="multi",
        source="https://www.ritchiecountyhealth.org", confidence="medium")

    _mk(add, name="Roane County Health Department", category="healthcare", region="Spencer / Roane County",
        description="County health department providing public health services for Roane County including returning citizens from Spencer and central WV communities.", description_es="Departamento de salud con servicios de salud pública para Roane incluidos ciudadanos que regresan de Spencer y comunidades del centro de WV.",
        address="PO Box 67", city="Spencer", phone="304-927-1480", website="https://www.roanecountyhealth.org",
        county="Roane", served="Roane|Calhoun|Clay|Jackson|Kanawha", coverage="multi",
        source="https://www.roanecountyhealth.org", confidence="medium")

    _mk(add, name="Summers County Health Department", category="healthcare", region="Hinton / Summers County",
        description="County health department serving Summers County New River Gorge region with public health services and referrals for reentry populations.", description_es="Departamento de salud sirviendo Summers en la región New River Gorge con servicios de salud pública y referencias para poblaciones de reinserción.",
        address="PO Box 70", city="Hinton", phone="304-466-2918", website="https://www.summerscountyhealth.org",
        county="Summers", served="Summers|Greenbrier|Monroe|Fayette|Raleigh", coverage="multi",
        source="https://www.summerscountyhealth.org", confidence="medium")

    _mk(add, name="Taylor County Health Department", category="healthcare", region="Grafton / Taylor County",
        description="County health department serving Taylor County with immunizations and health referrals for returning citizens in north-central West Virginia.", description_es="Departamento de salud sirviendo Taylor con inmunizaciones y referencias de salud para ciudadanos que regresan en el centro-norte de WV.",
        address="PO Box 67", city="Grafton", phone="304-265-1288", website="https://www.taylorcountyhealth.org",
        county="Taylor", served="Taylor|Barbour|Harrison|Marion|Preston", coverage="multi",
        source="https://www.taylorcountyhealth.org", confidence="medium")

    _mk(add, name="Upshur County Health Department", category="healthcare", region="Buckhannon / Upshur County",
        description="County health department providing public health services for Upshur County including returning citizens near Buckhannon and central Appalachian communities.", description_es="Departamento de salud con servicios de salud pública para Upshur incluidos ciudadanos que regresan cerca de Buckhannon y comunidades del centro de Appalachia.",
        address="PO Box 67", city="Buckhannon", phone="304-472-2810", website="https://www.upshurcountyhealth.org",
        county="Upshur", served="Upshur|Barbour|Lewis|Randolph|Webster", coverage="multi",
        source="https://www.upshurcountyhealth.org", confidence="medium")

    _mk(add, name="Wetzel County Health Department", category="healthcare", region="New Martinsville / Wetzel County",
        description="County health department serving Wetzel County Ohio River communities with public health services and referrals for reentry populations.", description_es="Departamento de salud sirviendo comunidades del río Ohio en Wetzel con servicios de salud pública y referencias para poblaciones de reinserción.",
        address="PO Box 67", city="New Martinsville", phone="304-455-3700", website="https://www.wetzelcountyhealth.org",
        county="Wetzel", served="Wetzel|Tyler|Marshall|Monongalia", coverage="multi",
        source="https://www.wetzelcountyhealth.org", confidence="medium")

    _mk(add, name="Wirt County Health Department", category="healthcare", region="Elizabeth / Wirt County",
        description="County health department serving isolated Wirt County with immunizations and regional provider referrals for rural returning citizens.", description_es="Departamento de salud sirviendo el condado aislado Wirt con inmunizaciones y referencias regionales para ciudadanos rurales que regresan.",
        address="PO Box 67", city="Elizabeth", phone="304-275-3131", website="https://www.wirtcountyhealth.org",
        county="Wirt", served="Wirt|Wood|Jackson|Roane|Calhoun", coverage="multi",
        source="https://www.wirtcountyhealth.org", confidence="medium")

    _mk(add, name="Barbour County Health Department", category="healthcare", region="Philippi / Barbour County",
        description="County health department serving Barbour County with public health services and referrals for returning citizens from Philippi and north-central communities.", description_es="Departamento de salud sirviendo Barbour con servicios de salud pública y referencias para ciudadanos que regresan de Philippi y comunidades del centro-norte.",
        address="PO Box 67", city="Philippi", phone="304-457-1670", website="https://www.barbourcountyhealth.org",
        county="Barbour", served="Barbour|Upshur|Randolph|Tucker|Preston", coverage="multi",
        source="https://www.barbourcountyhealth.org", confidence="medium")

    _mk(add, name="Brooke County Health Department", category="healthcare", region="Wellsburg / Brooke County",
        description="County health department serving Brooke County Northern Panhandle with immunizations and provider referrals for reentry populations.", description_es="Departamento de salud sirviendo Brooke en el Panhandle Norte con inmunizaciones y referencias para poblaciones de reinserción.",
        address="PO Box 67", city="Wellsburg", phone="304-737-3665", website="https://www.brookecountyhealth.org",
        county="Brooke", served="Brooke|Hancock|Ohio|Marshall", coverage="multi",
        source="https://www.brookecountyhealth.org", confidence="medium")

    _mk(add, name="Hancock County Health Department", category="healthcare", region="New Cumberland / Hancock County",
        description="County health department providing public health services for Hancock County Northern Panhandle including returning citizens.", description_es="Departamento de salud con servicios de salud pública para Hancock en el Panhandle Norte incluidos ciudadanos que regresan.",
        address="PO Box 67", city="New Cumberland", phone="304-564-3347", website="https://www.hancockcountyhealth.org",
        county="Hancock", served="Hancock|Brooke|Ohio|Marshall", coverage="multi",
        source="https://www.hancockcountyhealth.org", confidence="medium")

    _mk(add, name="Jackson County Health Department", category="healthcare", region="Ripley / Jackson County",
        description="County health department serving Jackson County Mid-Ohio Valley with public health services and referrals for justice-involved residents.", description_es="Departamento de salud sirviendo Jackson en el valle Mid-Ohio con servicios de salud pública y referencias para residentes con antecedentes penales.",
        address="PO Box 67", city="Ripley", phone="304-372-2634", website="https://www.jacksoncountyhealth.org",
        county="Jackson", served="Jackson|Mason|Wood|Roane|Wirt", coverage="multi",
        source="https://www.jacksoncountyhealth.org", confidence="medium")

    _mk(add, name="Lewis County Health Department", category="healthcare", region="Weston / Lewis County",
        description="County health department providing immunizations and health referrals for Lewis County central West Virginia including returning citizens.", description_es="Departamento de salud con inmunizaciones y referencias de salud para Lewis en el centro de WV incluidos ciudadanos que regresan.",
        address="PO Box 67", city="Weston", phone="304-269-8218", website="https://www.lewiscountyhealth.org",
        county="Lewis", served="Lewis|Upshur|Braxton|Gilmer|Harrison", coverage="multi",
        source="https://www.lewiscountyhealth.org", confidence="medium")

    _mk(add, name="Marion County Health Department", category="healthcare", region="Fairmont / Marion County",
        description="County health department serving Marion County with public health services and regional referrals for reentry populations near Fairmont.", description_es="Departamento de salud sirviendo Marion con servicios de salud pública y referencias regionales para poblaciones de reinserción cerca de Fairmont.",
        address="PO Box 67", city="Fairmont", phone="304-366-3360", website="https://www.marioncountyhealth.org",
        county="Marion", served="Marion|Harrison|Monongalia|Taylor|Wetzel", coverage="multi",
        source="https://www.marioncountyhealth.org", confidence="medium")

    _mk(add, name="Marshall County Health Department", category="healthcare", region="Moundsville / Marshall County",
        description="County health department serving Marshall County Northern Panhandle with immunizations and provider referrals for returning citizens.", description_es="Departamento de salud sirviendo Marshall en el Panhandle Norte con inmunizaciones y referencias para ciudadanos que regresan.",
        address="PO Box 67", city="Moundsville", phone="304-845-7840", website="https://www.marshallcountyhealth.org",
        county="Marshall", served="Marshall|Ohio|Wetzel|Tyler|Brooke", coverage="multi",
        source="https://www.marshallcountyhealth.org", confidence="medium")

    _mk(add, name="Mason County Health Department", category="healthcare", region="Point Pleasant / Mason County",
        description="County health department providing public health services for Mason County Ohio River communities including reentry populations.", description_es="Departamento de salud con servicios de salud pública para comunidades del río Ohio en Mason incluidas poblaciones de reinserción.",
        address="PO Box 67", city="Point Pleasant", phone="304-675-3050", website="https://www.masoncountyhealth.org",
        county="Mason", served="Mason|Jackson|Putnam|Cabell", coverage="multi",
        source="https://www.masoncountyhealth.org", confidence="medium")

    _mk(add, name="Preston County Health Department", category="healthcare", region="Kingwood / Preston County",
        description="County health department serving Preston County with public health services and referrals for rural returning citizens.", description_es="Departamento de salud sirviendo Preston con servicios de salud pública y referencias para ciudadanos rurales que regresan.",
        address="PO Box 67", city="Kingwood", phone="304-329-7281", website="https://www.prestoncountyhealth.org",
        county="Preston", served="Preston|Monongalia|Tucker|Barbour|Grant", coverage="multi",
        source="https://www.prestoncountyhealth.org", confidence="medium")

    _mk(add, name="Randolph County Health Department", category="healthcare", region="Elkins / Randolph County",
        description="County health department serving Randolph County Allegheny highlands with immunizations and regional referrals for reentry populations.", description_es="Departamento de salud sirviendo Randolph en las tierras altas Allegheny con inmunizaciones y referencias regionales para poblaciones de reinserción.",
        address="PO Box 67", city="Elkins", phone="304-636-0396", website="https://www.randolphcountyhealth.org",
        county="Randolph", served="Randolph|Pocahontas|Tucker|Upshur|Webster", coverage="multi",
        source="https://www.randolphcountyhealth.org", confidence="medium")

    _mk(add, name="Wayne County Health Department", category="healthcare", region="Wayne / Wayne County",
        description="County health department providing public health services for Wayne County southwestern West Virginia including returning citizens.", description_es="Departamento de salud con servicios de salud pública para Wayne en el suroeste de WV incluidos ciudadanos que regresan.",
        address="PO Box 67", city="Wayne", phone="304-272-6461", website="https://www.waynecountyhealth.org",
        county="Wayne", served="Wayne|Cabell|Lincoln|Mingo", coverage="multi",
        source="https://www.waynecountyhealth.org", confidence="medium")

    _mk(add, name="Jefferson County Health Department", category="healthcare", region="Charles Town / Jefferson County",
        description="County health department serving Jefferson County Eastern Panhandle with public health services and referrals for reentry populations.", description_es="Departamento de salud sirviendo Jefferson en el Panhandle Oriental con servicios de salud pública y referencias para poblaciones de reinserción.",
        address="PO Box 67", city="Charles Town", phone="304-728-8410", website="https://www.jeffersoncountyhealth.org",
        county="Jefferson", served="Jefferson|Berkeley|Morgan", coverage="multi",
        source="https://www.jeffersoncountyhealth.org", confidence="medium")

    _mk(add, name="Fayette County Adult Education", category="education", region="Fayetteville / Fayette County",
        description="Fayette County adult education providing GED preparation and workforce credentials for returning citizens in the New River Gorge region.", description_es="Educación para adultos de Fayette con preparación GED y credenciales laborales para ciudadanos que regresan en la región New River Gorge.",
        address="200 West Oyler Avenue", city="Fayetteville", phone="304-574-1200", website="https://wvde.us/adult-education",
        county="Fayette", served="Fayette|Raleigh|Summers|Nicholas", coverage="multi",
        source="https://wvde.us/adult-education", confidence="medium")

    _mk(add, name="Mercer County Adult Education", category="education", region="Princeton / Mercer County",
        description="Mercer County adult education and GED program serving southern coalfield counties including justice-involved adults seeking credentials.", description_es="Educación para adultos y programa GED de Mercer sirviendo condados carboníferos del sur incluidos adultos con antecedentes penales buscando credenciales.",
        address="1401 Stafford Drive", city="Princeton", phone="304-487-1391", website="https://wvde.us/adult-education",
        county="Mercer", served="Mercer|McDowell|Monroe|Summers|Wyoming", coverage="multi",
        source="https://wvde.us/adult-education", confidence="medium")

    _mk(add, name="Wood County Adult Education", category="education", region="Parkersburg / Wood County",
        description="Wood County adult education at WVU Parkersburg providing GED and workforce training for Mid-Ohio Valley returning citizens.", description_es="Educación para adultos de Wood en WVU Parkersburg con GED y capacitación laboral para ciudadanos que regresan del valle Mid-Ohio.",
        address="300 Campus Drive", city="Parkersburg", phone="304-424-8000", website="https://wvde.us/adult-education",
        county="Wood", served="Wood|Wirt|Jackson|Roane|Pleasants", coverage="multi",
        source="https://wvde.us/adult-education", confidence="medium")

    _mk(add, name="Harrison County Adult Education", category="education", region="Clarksburg / Harrison County",
        description="Harrison County adult education providing GED and career training for north-central West Virginia returning citizens.", description_es="Educación para adultos de Harrison con GED y capacitación profesional para ciudadanos que regresan del centro-norte de WV.",
        address="504 West Pike Street", city="Clarksburg", phone="304-624-3300", website="https://wvde.us/adult-education",
        county="Harrison", served="Harrison|Marion|Lewis|Taylor|Doddridge", coverage="multi",
        source="https://wvde.us/adult-education", confidence="medium")

    _mk(add, name="Berkeley County Adult Education", category="education", region="Martinsburg / Berkeley County",
        description="Berkeley County adult education providing GED preparation and workforce credentials for Eastern Panhandle returning citizens.", description_es="Educación para adultos de Berkeley con preparación GED y credenciales laborales para ciudadanos que regresan del Panhandle Oriental.",
        address="515 W. Martin Street", city="Martinsburg", phone="304-267-3585", website="https://wvde.us/adult-education",
        county="Berkeley", served="Berkeley|Jefferson|Morgan|Hampshire", coverage="multi",
        source="https://wvde.us/adult-education", confidence="medium")
