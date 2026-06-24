"""West Virginia Pass 2: metros, WVDCR parole offices, regional anchors."""

from west_virginia_resources_data import _mk, PAROLE_OFFICES, WV_DCR


def register_pass2(add):
    """Register parole offices and major metro program-level resources."""

    _mk(add, name="WVDCR — Beckley Parole Office", category="probation-parole", region="Beckley / Raleigh County",
        description="WVDCR — Beckley Parole Office supervises West Virginia parolees and interstate compact probationers in 8 counties through active community supervision, compliance monitoring, and referrals to local reentry partners. Parole officers connect supervisees to housing, treatment, employment, and DoHS benefits resources after release from WVDCR custody—not emergency crisis navigation or cash assistance. Southern District Region 3: Fayette, Greenbrier, Nicholas, Pocahontas, Raleigh and surrounding southeastern counties.", description_es="WVDCR — Beckley Parole Office supervisa a personas en libertad condicional de Virginia Occidental y probatoria interestatal en 8 condados mediante supervisión comunitaria activa, monitoreo de cumplimiento y referencias a aliados locales de reinserción. Los oficiales conectan a supervisados con vivienda, tratamiento, empleo y beneficios DoHS después de la liberación—no navegación de crisis ni efectivo.",
        address="110 S. Eisenhower Drive", city="Beckley", phone="304-256-6720", website="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx",
        county="Raleigh", served="Fayette|Greenbrier|Nicholas|Pocahontas|Raleigh|Summers|Webster|Wyoming", coverage="multi",
        services="Parole supervision|Compliance monitoring|Reentry partner referrals|Interstate compact supervision|Community resource navigation",
        tags="parole|WVDCR|raleigh|reentry|probation-parole",
        eligibility="West Virginia parolees and interstate compact supervisees assigned to this office; reporting requirements set by parole board and officer.",
        eligibility_es="Personas en libertad condicional de WV y supervisados del pacto interestatal asignados a esta oficina; requisitos de informe establecidos por la junta y el oficial.",
        notes="Report to your assigned parole officer at this office; call 304-256-6720 for office hours; not a walk-in benefits or housing intake site.",
        notes_es="Informe a su oficial de libertad condicional asignado; llame al 304-256-6720 para horarios; no es admisión de beneficios o vivienda.",
        source="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx", source_type="government")

    _mk(add, name="WVDCR — Charleston Parole Office", category="probation-parole", region="Charleston / Kanawha County",
        description="WVDCR — Charleston Parole Office supervises West Virginia parolees and interstate compact probationers in 7 counties through active community supervision, compliance monitoring, and referrals to local reentry partners. Parole officers connect supervisees to housing, treatment, employment, and DoHS benefits resources after release from WVDCR custody—not emergency crisis navigation or cash assistance. Southern District Region 2: Boone, Clay, Jackson, Kanawha, Logan, Mingo, and Roane counties.", description_es="WVDCR — Charleston Parole Office supervisa a personas en libertad condicional de Virginia Occidental y probatoria interestatal en 7 condados mediante supervisión comunitaria activa, monitoreo de cumplimiento y referencias a aliados locales de reinserción. Los oficiales conectan a supervisados con vivienda, tratamiento, empleo y beneficios DoHS después de la liberación—no navegación de crisis ni efectivo.",
        address="1356 Hansford Street, Suite B", city="Charleston", phone="304-558-3597", website="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx",
        county="Kanawha", served="Boone|Clay|Jackson|Kanawha|Logan|Mingo|Roane", coverage="multi",
        services="Parole supervision|Compliance monitoring|Reentry partner referrals|Interstate compact supervision|Community resource navigation",
        tags="parole|WVDCR|kanawha|reentry|probation-parole",
        eligibility="West Virginia parolees and interstate compact supervisees assigned to this office; reporting requirements set by parole board and officer.",
        eligibility_es="Personas en libertad condicional de WV y supervisados del pacto interestatal asignados a esta oficina; requisitos de informe establecidos por la junta y el oficial.",
        notes="Report to your assigned parole officer at this office; call 304-558-3597 for office hours; not a walk-in benefits or housing intake site.",
        notes_es="Informe a su oficial de libertad condicional asignado; llame al 304-558-3597 para horarios; no es admisión de beneficios o vivienda.",
        source="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx", source_type="government")

    _mk(add, name="WVDCR — Clarksburg Parole Office", category="probation-parole", region="Clarksburg / Harrison County",
        description="WVDCR — Clarksburg Parole Office supervises West Virginia parolees and interstate compact probationers in 10 counties through active community supervision, compliance monitoring, and referrals to local reentry partners. Parole officers connect supervisees to housing, treatment, employment, and DoHS benefits resources after release from WVDCR custody—not emergency crisis navigation or cash assistance. Northern District Region 6: north-central West Virginia including Harrison, Marion, and Monongalia counties.", description_es="WVDCR — Clarksburg Parole Office supervisa a personas en libertad condicional de Virginia Occidental y probatoria interestatal en 10 condados mediante supervisión comunitaria activa, monitoreo de cumplimiento y referencias a aliados locales de reinserción. Los oficiales conectan a supervisados con vivienda, tratamiento, empleo y beneficios DoHS después de la liberación—no navegación de crisis ni efectivo.",
        address="200 West Main Street", city="Clarksburg", phone="304-624-2000", website="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx",
        county="Harrison", served="Barbour|Braxton|Doddridge|Harrison|Lewis|Marion|Monongalia|Preston|Taylor|Upshur", coverage="multi",
        services="Parole supervision|Compliance monitoring|Reentry partner referrals|Interstate compact supervision|Community resource navigation",
        tags="parole|WVDCR|harrison|reentry|probation-parole",
        eligibility="West Virginia parolees and interstate compact supervisees assigned to this office; reporting requirements set by parole board and officer.",
        eligibility_es="Personas en libertad condicional de WV y supervisados del pacto interestatal asignados a esta oficina; requisitos de informe establecidos por la junta y el oficial.",
        notes="Report to your assigned parole officer at this office; call 304-624-2000 for office hours; not a walk-in benefits or housing intake site.",
        notes_es="Informe a su oficial de libertad condicional asignado; llame al 304-624-2000 para horarios; no es admisión de beneficios o vivienda.",
        source="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx", source_type="government")

    _mk(add, name="WVDCR — Elkins Parole Office", category="probation-parole", region="Elkins / Randolph County",
        description="WVDCR — Elkins Parole Office supervises West Virginia parolees and interstate compact probationers in 4 counties through active community supervision, compliance monitoring, and referrals to local reentry partners. Parole officers connect supervisees to housing, treatment, employment, and DoHS benefits resources after release from WVDCR custody—not emergency crisis navigation or cash assistance. Northern District Region 6: Randolph, Pendleton, Tucker, and Webster counties in the Allegheny highlands.", description_es="WVDCR — Elkins Parole Office supervisa a personas en libertad condicional de Virginia Occidental y probatoria interestatal en 4 condados mediante supervisión comunitaria activa, monitoreo de cumplimiento y referencias a aliados locales de reinserción. Los oficiales conectan a supervisados con vivienda, tratamiento, empleo y beneficios DoHS después de la liberación—no navegación de crisis ni efectivo.",
        address="1023 North Randolph Avenue", city="Elkins", phone="304-637-0250", website="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx",
        county="Randolph", served="Pendleton|Randolph|Tucker|Webster", coverage="multi",
        services="Parole supervision|Compliance monitoring|Reentry partner referrals|Interstate compact supervision|Community resource navigation",
        tags="parole|WVDCR|randolph|reentry|probation-parole",
        eligibility="West Virginia parolees and interstate compact supervisees assigned to this office; reporting requirements set by parole board and officer.",
        eligibility_es="Personas en libertad condicional de WV y supervisados del pacto interestatal asignados a esta oficina; requisitos de informe establecidos por la junta y el oficial.",
        notes="Report to your assigned parole officer at this office; call 304-637-0250 for office hours; not a walk-in benefits or housing intake site.",
        notes_es="Informe a su oficial de libertad condicional asignado; llame al 304-637-0250 para horarios; no es admisión de beneficios o vivienda.",
        source="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx", source_type="government")

    _mk(add, name="WVDCR — Huntington Parole Office", category="probation-parole", region="Huntington / Cabell County",
        description="WVDCR — Huntington Parole Office supervises West Virginia parolees and interstate compact probationers in 5 counties through active community supervision, compliance monitoring, and referrals to local reentry partners. Parole officers connect supervisees to housing, treatment, employment, and DoHS benefits resources after release from WVDCR custody—not emergency crisis navigation or cash assistance. Southern District Region 1: Cabell, Lincoln, Mason, Putnam, and Wayne counties in the Metro Valley.", description_es="WVDCR — Huntington Parole Office supervisa a personas en libertad condicional de Virginia Occidental y probatoria interestatal en 5 condados mediante supervisión comunitaria activa, monitoreo de cumplimiento y referencias a aliados locales de reinserción. Los oficiales conectan a supervisados con vivienda, tratamiento, empleo y beneficios DoHS después de la liberación—no navegación de crisis ni efectivo.",
        address="2699 Park Avenue, Suite 200", city="Huntington", phone="304-528-5060", website="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx",
        county="Cabell", served="Cabell|Lincoln|Mason|Putnam|Wayne", coverage="multi",
        services="Parole supervision|Compliance monitoring|Reentry partner referrals|Interstate compact supervision|Community resource navigation",
        tags="parole|WVDCR|cabell|reentry|probation-parole",
        eligibility="West Virginia parolees and interstate compact supervisees assigned to this office; reporting requirements set by parole board and officer.",
        eligibility_es="Personas en libertad condicional de WV y supervisados del pacto interestatal asignados a esta oficina; requisitos de informe establecidos por la junta y el oficial.",
        notes="Report to your assigned parole officer at this office; call 304-528-5060 for office hours; not a walk-in benefits or housing intake site.",
        notes_es="Informe a su oficial de libertad condicional asignado; llame al 304-528-5060 para horarios; no es admisión de beneficios o vivienda.",
        source="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx", source_type="government")

    _mk(add, name="WVDCR — Lewisburg Parole Office", category="probation-parole", region="Lewisburg / Greenbrier County",
        description="WVDCR — Lewisburg Parole Office supervises West Virginia parolees and interstate compact probationers in 3 counties through active community supervision, compliance monitoring, and referrals to local reentry partners. Parole officers connect supervisees to housing, treatment, employment, and DoHS benefits resources after release from WVDCR custody—not emergency crisis navigation or cash assistance. Southern District Region 3: Greenbrier, Monroe, and Summers counties in the Greenbrier Valley.", description_es="WVDCR — Lewisburg Parole Office supervisa a personas en libertad condicional de Virginia Occidental y probatoria interestatal en 3 condados mediante supervisión comunitaria activa, monitoreo de cumplimiento y referencias a aliados locales de reinserción. Los oficiales conectan a supervisados con vivienda, tratamiento, empleo y beneficios DoHS después de la liberación—no navegación de crisis ni efectivo.",
        address="912 North Jefferson Street", city="Lewisburg", phone="304-647-7474", website="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx",
        county="Greenbrier", served="Greenbrier|Monroe|Summers", coverage="multi",
        services="Parole supervision|Compliance monitoring|Reentry partner referrals|Interstate compact supervision|Community resource navigation",
        tags="parole|WVDCR|greenbrier|reentry|probation-parole",
        eligibility="West Virginia parolees and interstate compact supervisees assigned to this office; reporting requirements set by parole board and officer.",
        eligibility_es="Personas en libertad condicional de WV y supervisados del pacto interestatal asignados a esta oficina; requisitos de informe establecidos por la junta y el oficial.",
        notes="Report to your assigned parole officer at this office; call 304-647-7474 for office hours; not a walk-in benefits or housing intake site.",
        notes_es="Informe a su oficial de libertad condicional asignado; llame al 304-647-7474 para horarios; no es admisión de beneficios o vivienda.",
        source="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx", source_type="government")

    _mk(add, name="WVDCR — Logan Parole Office", category="probation-parole", region="Logan / Logan County",
        description="WVDCR — Logan Parole Office supervises West Virginia parolees and interstate compact probationers in 3 counties through active community supervision, compliance monitoring, and referrals to local reentry partners. Parole officers connect supervisees to housing, treatment, employment, and DoHS benefits resources after release from WVDCR custody—not emergency crisis navigation or cash assistance. Southern District Region 2: Boone, Logan, and Mingo counties in the coalfields.", description_es="WVDCR — Logan Parole Office supervisa a personas en libertad condicional de Virginia Occidental y probatoria interestatal en 3 condados mediante supervisión comunitaria activa, monitoreo de cumplimiento y referencias a aliados locales de reinserción. Los oficiales conectan a supervisados con vivienda, tratamiento, empleo y beneficios DoHS después de la liberación—no navegación de crisis ni efectivo.",
        address="1000 State Route 10", city="Logan", phone="304-792-7020", website="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx",
        county="Logan", served="Boone|Logan|Mingo", coverage="multi",
        services="Parole supervision|Compliance monitoring|Reentry partner referrals|Interstate compact supervision|Community resource navigation",
        tags="parole|WVDCR|logan|reentry|probation-parole",
        eligibility="West Virginia parolees and interstate compact supervisees assigned to this office; reporting requirements set by parole board and officer.",
        eligibility_es="Personas en libertad condicional de WV y supervisados del pacto interestatal asignados a esta oficina; requisitos de informe establecidos por la junta y el oficial.",
        notes="Report to your assigned parole officer at this office; call 304-792-7020 for office hours; not a walk-in benefits or housing intake site.",
        notes_es="Informe a su oficial de libertad condicional asignado; llame al 304-792-7020 para horarios; no es admisión de beneficios o vivienda.",
        source="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx", source_type="government")

    _mk(add, name="WVDCR — Martinsburg Parole Office", category="probation-parole", region="Martinsburg / Berkeley County",
        description="WVDCR — Martinsburg Parole Office supervises West Virginia parolees and interstate compact probationers in 7 counties through active community supervision, compliance monitoring, and referrals to local reentry partners. Parole officers connect supervisees to housing, treatment, employment, and DoHS benefits resources after release from WVDCR custody—not emergency crisis navigation or cash assistance. Northern District Region 7: Eastern Panhandle counties including Berkeley and Jefferson.", description_es="WVDCR — Martinsburg Parole Office supervisa a personas en libertad condicional de Virginia Occidental y probatoria interestatal en 7 condados mediante supervisión comunitaria activa, monitoreo de cumplimiento y referencias a aliados locales de reinserción. Los oficiales conectan a supervisados con vivienda, tratamiento, empleo y beneficios DoHS después de la liberación—no navegación de crisis ni efectivo.",
        address="510 North Queen Street", city="Martinsburg", phone="304-263-0611", website="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx",
        county="Berkeley", served="Berkeley|Grant|Hampshire|Hardy|Jefferson|Mineral|Morgan", coverage="multi",
        services="Parole supervision|Compliance monitoring|Reentry partner referrals|Interstate compact supervision|Community resource navigation",
        tags="parole|WVDCR|berkeley|reentry|probation-parole",
        eligibility="West Virginia parolees and interstate compact supervisees assigned to this office; reporting requirements set by parole board and officer.",
        eligibility_es="Personas en libertad condicional de WV y supervisados del pacto interestatal asignados a esta oficina; requisitos de informe establecidos por la junta y el oficial.",
        notes="Report to your assigned parole officer at this office; call 304-263-0611 for office hours; not a walk-in benefits or housing intake site.",
        notes_es="Informe a su oficial de libertad condicional asignado; llame al 304-263-0611 para horarios; no es admisión de beneficios o vivienda.",
        source="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx", source_type="government")

    _mk(add, name="WVDCR — Moorefield Parole Office", category="probation-parole", region="Moorefield / Hardy County",
        description="WVDCR — Moorefield Parole Office supervises West Virginia parolees and interstate compact probationers in 3 counties through active community supervision, compliance monitoring, and referrals to local reentry partners. Parole officers connect supervisees to housing, treatment, employment, and DoHS benefits resources after release from WVDCR custody—not emergency crisis navigation or cash assistance. Northern District Region 7: Grant, Hardy, and Pendleton counties in the Potomac Highlands.", description_es="WVDCR — Moorefield Parole Office supervisa a personas en libertad condicional de Virginia Occidental y probatoria interestatal en 3 condados mediante supervisión comunitaria activa, monitoreo de cumplimiento y referencias a aliados locales de reinserción. Los oficiales conectan a supervisados con vivienda, tratamiento, empleo y beneficios DoHS después de la liberación—no navegación de crisis ni efectivo.",
        address="819 North Main Street", city="Moorefield", phone="304-538-2700", website="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx",
        county="Hardy", served="Grant|Hardy|Pendleton", coverage="multi",
        services="Parole supervision|Compliance monitoring|Reentry partner referrals|Interstate compact supervision|Community resource navigation",
        tags="parole|WVDCR|hardy|reentry|probation-parole",
        eligibility="West Virginia parolees and interstate compact supervisees assigned to this office; reporting requirements set by parole board and officer.",
        eligibility_es="Personas en libertad condicional de WV y supervisados del pacto interestatal asignados a esta oficina; requisitos de informe establecidos por la junta y el oficial.",
        notes="Report to your assigned parole officer at this office; call 304-538-2700 for office hours; not a walk-in benefits or housing intake site.",
        notes_es="Informe a su oficial de libertad condicional asignado; llame al 304-538-2700 para horarios; no es admisión de beneficios o vivienda.",
        source="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx", source_type="government")

    _mk(add, name="WVDCR — Parkersburg Parole Office", category="probation-parole", region="Parkersburg / Wood County",
        description="WVDCR — Parkersburg Parole Office supervises West Virginia parolees and interstate compact probationers in 8 counties through active community supervision, compliance monitoring, and referrals to local reentry partners. Parole officers connect supervisees to housing, treatment, employment, and DoHS benefits resources after release from WVDCR custody—not emergency crisis navigation or cash assistance. Northern District Region 5: Mid-Ohio Valley counties including Wood and Jackson.", description_es="WVDCR — Parkersburg Parole Office supervisa a personas en libertad condicional de Virginia Occidental y probatoria interestatal en 8 condados mediante supervisión comunitaria activa, monitoreo de cumplimiento y referencias a aliados locales de reinserción. Los oficiales conectan a supervisados con vivienda, tratamiento, empleo y beneficios DoHS después de la liberación—no navegación de crisis ni efectivo.",
        address="1515 Murdoch Avenue", city="Parkersburg", phone="304-420-4500", website="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx",
        county="Wood", served="Calhoun|Clay|Jackson|Pleasants|Ritchie|Roane|Wirt|Wood", coverage="multi",
        services="Parole supervision|Compliance monitoring|Reentry partner referrals|Interstate compact supervision|Community resource navigation",
        tags="parole|WVDCR|wood|reentry|probation-parole",
        eligibility="West Virginia parolees and interstate compact supervisees assigned to this office; reporting requirements set by parole board and officer.",
        eligibility_es="Personas en libertad condicional de WV y supervisados del pacto interestatal asignados a esta oficina; requisitos de informe establecidos por la junta y el oficial.",
        notes="Report to your assigned parole officer at this office; call 304-420-4500 for office hours; not a walk-in benefits or housing intake site.",
        notes_es="Informe a su oficial de libertad condicional asignado; llame al 304-420-4500 para horarios; no es admisión de beneficios o vivienda.",
        source="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx", source_type="government")

    _mk(add, name="WVDCR — Princeton Parole Office", category="probation-parole", region="Princeton / Mercer County",
        description="WVDCR — Princeton Parole Office supervises West Virginia parolees and interstate compact probationers in 5 counties through active community supervision, compliance monitoring, and referrals to local reentry partners. Parole officers connect supervisees to housing, treatment, employment, and DoHS benefits resources after release from WVDCR custody—not emergency crisis navigation or cash assistance. Southern District Region 4: McDowell, Mercer, Monroe, Summers, and Wyoming counties.", description_es="WVDCR — Princeton Parole Office supervisa a personas en libertad condicional de Virginia Occidental y probatoria interestatal en 5 condados mediante supervisión comunitaria activa, monitoreo de cumplimiento y referencias a aliados locales de reinserción. Los oficiales conectan a supervisados con vivienda, tratamiento, empleo y beneficios DoHS después de la liberación—no navegación de crisis ni efectivo.",
        address="200 Mercer Street", city="Princeton", phone="304-487-3500", website="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx",
        county="Mercer", served="McDowell|Mercer|Monroe|Summers|Wyoming", coverage="multi",
        services="Parole supervision|Compliance monitoring|Reentry partner referrals|Interstate compact supervision|Community resource navigation",
        tags="parole|WVDCR|mercer|reentry|probation-parole",
        eligibility="West Virginia parolees and interstate compact supervisees assigned to this office; reporting requirements set by parole board and officer.",
        eligibility_es="Personas en libertad condicional de WV y supervisados del pacto interestatal asignados a esta oficina; requisitos de informe establecidos por la junta y el oficial.",
        notes="Report to your assigned parole officer at this office; call 304-487-3500 for office hours; not a walk-in benefits or housing intake site.",
        notes_es="Informe a su oficial de libertad condicional asignado; llame al 304-487-3500 para horarios; no es admisión de beneficios o vivienda.",
        source="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx", source_type="government")

    _mk(add, name="WVDCR — Welch Parole Office", category="probation-parole", region="Welch / McDowell County",
        description="WVDCR — Welch Parole Office supervises West Virginia parolees and interstate compact probationers in 3 counties through active community supervision, compliance monitoring, and referrals to local reentry partners. Parole officers connect supervisees to housing, treatment, employment, and DoHS benefits resources after release from WVDCR custody—not emergency crisis navigation or cash assistance. Southern District Region 4: McDowell, Mingo, and Wyoming counties in southern coalfield communities.", description_es="WVDCR — Welch Parole Office supervisa a personas en libertad condicional de Virginia Occidental y probatoria interestatal en 3 condados mediante supervisión comunitaria activa, monitoreo de cumplimiento y referencias a aliados locales de reinserción. Los oficiales conectan a supervisados con vivienda, tratamiento, empleo y beneficios DoHS después de la liberación—no navegación de crisis ni efectivo.",
        address="140 Main Street", city="Welch", phone="304-436-4200", website="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx",
        county="McDowell", served="McDowell|Mingo|Wyoming", coverage="multi",
        services="Parole supervision|Compliance monitoring|Reentry partner referrals|Interstate compact supervision|Community resource navigation",
        tags="parole|WVDCR|mcdowell|reentry|probation-parole",
        eligibility="West Virginia parolees and interstate compact supervisees assigned to this office; reporting requirements set by parole board and officer.",
        eligibility_es="Personas en libertad condicional de WV y supervisados del pacto interestatal asignados a esta oficina; requisitos de informe establecidos por la junta y el oficial.",
        notes="Report to your assigned parole officer at this office; call 304-436-4200 for office hours; not a walk-in benefits or housing intake site.",
        notes_es="Informe a su oficial de libertad condicional asignado; llame al 304-436-4200 para horarios; no es admisión de beneficios o vivienda.",
        source="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx", source_type="government")

    _mk(add, name="WVDCR — Wheeling Parole Office", category="probation-parole", region="Wheeling / Ohio County",
        description="WVDCR — Wheeling Parole Office supervises West Virginia parolees and interstate compact probationers in 6 counties through active community supervision, compliance monitoring, and referrals to local reentry partners. Parole officers connect supervisees to housing, treatment, employment, and DoHS benefits resources after release from WVDCR custody—not emergency crisis navigation or cash assistance. Northern District Region 5: Northern Panhandle counties including Ohio, Marshall, and Hancock.", description_es="WVDCR — Wheeling Parole Office supervisa a personas en libertad condicional de Virginia Occidental y probatoria interestatal en 6 condados mediante supervisión comunitaria activa, monitoreo de cumplimiento y referencias a aliados locales de reinserción. Los oficiales conectan a supervisados con vivienda, tratamiento, empleo y beneficios DoHS después de la liberación—no navegación de crisis ni efectivo.",
        address="1058 East Bethlehem Boulevard", city="Wheeling", phone="304-238-0500", website="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx",
        county="Ohio", served="Brooke|Hancock|Marshall|Ohio|Tyler|Wetzel", coverage="multi",
        services="Parole supervision|Compliance monitoring|Reentry partner referrals|Interstate compact supervision|Community resource navigation",
        tags="parole|WVDCR|ohio|reentry|probation-parole",
        eligibility="West Virginia parolees and interstate compact supervisees assigned to this office; reporting requirements set by parole board and officer.",
        eligibility_es="Personas en libertad condicional de WV y supervisados del pacto interestatal asignados a esta oficina; requisitos de informe establecidos por la junta y el oficial.",
        notes="Report to your assigned parole officer at this office; call 304-238-0500 for office hours; not a walk-in benefits or housing intake site.",
        notes_es="Informe a su oficial de libertad condicional asignado; llame al 304-238-0500 para horarios; no es admisión de beneficios o vivienda.",
        source="https://dcr.wv.gov/facilities/Pages/parole-services-offices.aspx", source_type="government")

    _mk(add, name="Recovery Point of Huntington — Men's Recovery Housing", category="housing", region="Huntington / Cabell County",
        description="Faith-based long-term recovery residence providing structured sober living, life skills, and peer support for men in early recovery including justice-involved men referred from courts, probation, and regional jails in Cabell County.", description_es="Residencia de recuperación a largo plazo basada en la fe con vida sobria estructurada, habilidades para la vida y apoyo entre pares para hombres en recuperación temprana, incluidos hombres con antecedentes penales referidos por tribunales y probatoria en el condado Cabell.",
        address="1527 7th Avenue", city="Huntington", phone="304-523-4673", website="https://www.recoverypointwv.org",
        county="Cabell", served="Cabell", coverage="single",
        eligibility="Men in early recovery; justice referrals accepted from courts and corrections partners; sobriety required.",
        eligibility_es="Men in early recovery; justice referrals accepted from courts and corrections partners; sobriety required.",
        source="https://www.recoverypointwv.org")

    _mk(add, name="Prestera Center — Reentry Behavioral Health Services", category="substance-use-treatment", region="Charleston / Kanawha County",
        description="Community mental health center providing outpatient and residential substance use disorder treatment, MAT, crisis services, and care coordination for Medicaid and uninsured clients including justice-involved adults across the Kanawha Valley and southern coalfields.", description_es="Centro de salud mental comunitario con tratamiento ambulatorio y residencial de trastornos por uso de sustancias, TMO, servicios de crisis y coordinación de atención para clientes Medicaid y sin seguro, incluidos adultos con antecedentes penales en el valle Kanawha.",
        address="912 Quarrier Street", city="Charleston", phone="304-348-0531", website="https://www.prestera.org",
        county="Kanawha", served="Kanawha|Putnam|Boone|Clay|Lincoln|Logan|Mingo|Wayne", coverage="multi",
        eligibility="Medicaid and uninsured residents in served counties; intake assessment required; justice referrals accepted for many programs.",
        eligibility_es="Medicaid and uninsured residents in served counties; intake assessment required; justice referrals accepted for many programs.",
        source="https://www.prestera.org")

    _mk(add, name="West Virginia Health Right — Free & Charitable Clinic", category="healthcare", region="Charleston / Kanawha County",
        description="Free and charitable clinic providing primary care, chronic disease management, behavioral health, dental, vision, and medication assistance on a sliding scale for uninsured low-income West Virginians including returning citizens reestablishing medical care after release.", description_es="Clínica gratuita y benéfica con atención primaria, manejo de enfermedades crónicas, salud conductual, dental, visión y asistencia con medicamentos para virginianos occidentales de bajos ingresos sin seguro, incluidos ciudadanos que regresan.",
        address="1534 Washington Street East", city="Charleston", phone="304-414-5930", website="https://www.wvhealthright.org",
        county="Kanawha", served="Kanawha|Clay|Fayette|Boone|Lincoln|Logan|Mingo|Putnam|Wayne", coverage="multi",
        eligibility="Uninsured low-income adults in service area; criminal record not a stated barrier; appointment recommended.",
        eligibility_es="Uninsured low-income adults in service area; criminal record not a stated barrier; appointment recommended.",
        source="https://www.wvhealthright.org")

    _mk(add, name="Legal Aid of West Virginia — Charleston Office", category="legal-aid", region="Charleston / Kanawha County",
        description="Nonprofit civil legal aid serving low-income West Virginians with housing, public benefits, family law, consumer issues, and record expungement assistance under state Clean Slate and expungement statutes—not criminal defense.", description_es="Asistencia legal civil sin fines de lucro para virginianos occidentales de bajos ingresos con vivienda, beneficios públicos, derecho familiar y eliminación de antecedentes bajo estatutos estatales—no defensa penal.",
        address="901 Quarrier Street", city="Charleston", phone="866-255-4373", website="https://www.lawv.net",
        county="Kanawha", served="Kanawha|Boone|Clay|Fayette|Lincoln|Logan|Mingo|Putnam|Wayne", coverage="multi",
        eligibility="Low-income WV residents; LSC income limits apply; expungement eligibility depends on offense type and waiting periods.",
        eligibility_es="Low-income WV residents; LSC income limits apply; expungement eligibility depends on offense type and waiting periods.",
        source="https://www.lawv.net")

    _mk(add, name="Legal Aid of West Virginia — Huntington Office", category="legal-aid", region="Huntington / Cabell County",
        description="Regional civil legal aid office helping low-income residents in the Metro Valley with eviction defense, benefits appeals, family law, and criminal record expungement consultations for justice-involved clients.", description_es="Oficina regional de asistencia legal civil para residentes de bajos ingresos en el valle metropolitano con defensa contra desalojos, apelaciones de beneficios, derecho familiar y consultas de eliminación de antecedentes.",
        address="845 5th Avenue", city="Huntington", phone="866-255-4373", website="https://www.lawv.net",
        county="Cabell", served="Cabell|Lincoln|Mason|Putnam|Wayne", coverage="multi",
        eligibility="Low-income residents of served counties; intake through statewide hotline 866-255-4373 or local office.",
        eligibility_es="Low-income residents of served counties; intake through statewide hotline 866-255-4373 or local office.",
        source="https://www.lawv.net")

    _mk(add, name="Legal Aid of West Virginia — Martinsburg Office", category="legal-aid", region="Martinsburg / Berkeley County",
        description="Eastern Panhandle civil legal aid office serving low-income residents with housing, benefits, family law, and expungement assistance for justice-involved clients in Berkeley, Jefferson, and surrounding eastern counties.", description_es="Oficina de asistencia legal civil del Panhandle Oriental para residentes de bajos ingresos con vivienda, beneficios, derecho familiar y eliminación de antecedentes en condados orientales.",
        address="126 East Burke Street", city="Martinsburg", phone="866-255-4373", website="https://www.lawv.net",
        county="Berkeley", served="Berkeley|Grant|Hampshire|Hardy|Jefferson|Mineral|Morgan", coverage="multi",
        eligibility="Low-income Eastern Panhandle residents; call 866-255-4373 for intake routing.",
        eligibility_es="Low-income Eastern Panhandle residents; call 866-255-4373 for intake routing.",
        source="https://www.lawv.net")

    _mk(add, name="Legal Aid of West Virginia — Clarksburg Office", category="legal-aid", region="Clarksburg / Harrison County",
        description="North-central West Virginia civil legal aid office helping low-income residents with housing, benefits, family law, and record relief in Harrison, Marion, Monongalia, and surrounding counties.", description_es="Oficina de asistencia legal civil del centro-norte de WV para residentes de bajos ingresos con vivienda, beneficios, derecho familiar y alivio de antecedentes en Harrison, Marion y condados circundantes.",
        address="102 South Third Street", city="Clarksburg", phone="866-255-4373", website="https://www.lawv.net",
        county="Harrison", served="Barbour|Braxton|Doddridge|Gilmer|Harrison|Lewis|Marion|Monongalia|Preston|Taylor|Upshur", coverage="multi",
        eligibility="Low-income residents of served north-central counties; intake via 866-255-4373.",
        eligibility_es="Low-income residents of served north-central counties; intake via 866-255-4373.",
        source="https://www.lawv.net")

    _mk(add, name="Legal Aid of West Virginia — Wheeling Office", category="legal-aid", region="Wheeling / Ohio County",
        description="Northern Panhandle civil legal aid serving low-income residents in Brooke, Hancock, Marshall, Ohio, Tyler, and Wetzel counties with housing, benefits, and expungement legal help.", description_es="Asistencia legal civil del Panhandle Norte para residentes de bajos ingresos en Brooke, Hancock, Marshall, Ohio, Tyler y Wetzel con vivienda, beneficios y eliminación de antecedentes.",
        address="901 Main Street", city="Wheeling", phone="866-255-4373", website="https://www.lawv.net",
        county="Ohio", served="Brooke|Hancock|Marshall|Ohio|Tyler|Wetzel", coverage="multi",
        eligibility="Low-income Northern Panhandle residents; intake through 866-255-4373.",
        eligibility_es="Low-income Northern Panhandle residents; intake through 866-255-4373.",
        source="https://www.lawv.net")

    _mk(add, name="Community Care of West Virginia — Buckhannon Health Center", category="healthcare", region="Buckhannon / Upshur County",
        description="Federally qualified health center network providing primary care, dental, behavioral health, pharmacy, and sliding-fee services across north-central West Virginia including rural counties with limited reentry directories.", description_es="Red de centros de salud calificados federalmente con atención primaria, dental, salud conductual, farmacia y tarifa escalonada en el centro-norte de Virginia Occidental incluidos condados rurales.",
        address="37 West Main Street", city="Buckhannon", phone="304-472-1600", website="https://www.communitycarewv.org",
        county="Upshur", served="Braxton|Clay|Harrison|Lewis|Pocahontas|Randolph|Upshur", coverage="multi",
        eligibility="Open to residents of served counties; sliding fee based on income; Medicaid accepted; criminal record not a stated barrier.",
        eligibility_es="Open to residents of served counties; sliding fee based on income; Medicaid accepted; criminal record not a stated barrier.",
        source="https://www.communitycarewv.org")

    _mk(add, name="Valley Health Systems — Huntington Community Health Center", category="healthcare", region="Huntington / Cabell County",
        description="Federally qualified health center providing primary care, behavioral health, dental, and pharmacy services on sliding fee scale for uninsured and Medicaid patients in the Metro Valley including justice-involved individuals after release.", description_es="Centro de salud comunitario calificado federalmente con atención primaria, salud conductual, dental y farmacia con tarifa escalonada para pacientes sin seguro y Medicaid en el valle metropolitano.",
        address="5183 U.S. Route 60", city="Huntington", phone="304-522-0800", website="https://www.valleyhealth.org",
        county="Cabell", served="Cabell|Lincoln|Mason|Putnam|Wayne", coverage="multi",
        eligibility="Residents of served Metro Valley counties; sliding fee available; Medicaid and uninsured patients welcome.",
        eligibility_es="Residents of served Metro Valley counties; sliding fee available; Medicaid and uninsured patients welcome.",
        source="https://www.valleyhealth.org")

    _mk(add, name="FMRS Health Systems — Lewisburg Behavioral Health", category="healthcare", region="Lewisburg / Greenbrier County",
        description="Community mental health center providing outpatient behavioral health, substance use treatment, crisis services, and care coordination for Medicaid beneficiaries in southeastern West Virginia including rural reentry populations.", description_es="Centro de salud mental comunitario con salud conductual ambulatoria, tratamiento de uso de sustancias, crisis y coordinación de atención para beneficiarios Medicaid en el sureste de Virginia Occidental.",
        address="101 South Court Street", city="Lewisburg", phone="304-647-6451", website="https://www.fmrs.org",
        county="Greenbrier", served="Fayette|Greenbrier|Monroe|Pocahontas|Summers|Webster", coverage="multi",
        eligibility="Medicaid and publicly funded behavioral health clients in served counties; intake assessment required.",
        eligibility_es="Medicaid and publicly funded behavioral health clients in served counties; intake assessment required.",
        source="https://www.fmrs.org")

    _mk(add, name="Seneca Health Services — Summersville Behavioral Health", category="substance-use-treatment", region="Summersville / Nicholas County",
        description="Community behavioral health authority providing outpatient and residential substance use disorder treatment, crisis stabilization, and peer recovery supports for Medicaid clients in central Appalachian counties.", description_es="Autoridad de salud conductual comunitaria con tratamiento ambulatorio y residencial de trastornos por uso de sustancias, estabilización de crisis y apoyos de recuperación entre pares para clientes Medicaid.",
        address="804 Industrial Park Road", city="Summersville", phone="304-872-2651", website="https://www.senecahealth.org",
        county="Nicholas", served="Fayette|Greenbrier|Nicholas|Pocahontas|Webster|Wyoming", coverage="multi",
        eligibility="Medicaid and publicly funded behavioral health in served counties; justice referrals accepted for many programs.",
        eligibility_es="Medicaid and publicly funded behavioral health in served counties; justice referrals accepted for many programs.",
        source="https://www.senecahealth.org")

    _mk(add, name="North Central Community Action — Upshur County Services", category="basic-needs", region="Buckhannon / Upshur County",
        description="Community Action Agency providing emergency utility assistance, weatherization, food support referrals, and case management for low-income families in north-central West Virginia including returning citizens rebuilding household stability.", description_es="Agencia de Acción Comunitaria con asistencia de emergencia para servicios públicos, climatización, referencias de alimentos y manejo de casos para familias de bajos ingresos en el centro-norte de WV.",
        address="27 North Kanawha Street", city="Buckhannon", phone="304-472-7653", website="https://www.nccawv.org",
        county="Upshur", served="Barbour|Braxton|Gilmer|Lewis|Randolph|Upshur|Webster", coverage="multi",
        eligibility="Low-income residents of served counties; income verification required for emergency assistance programs.",
        eligibility_es="Low-income residents of served counties; income verification required for emergency assistance programs.",
        source="https://www.nccawv.org")

    _mk(add, name="Mountaineer Food Bank — Partner Agency Network", category="food-nutrition", region="Gassaway / Braxton County",
        description="Regional food bank distributing to partner pantries across north-central and eastern West Virginia helping returning citizens locate emergency food by ZIP code through the online food finder.", description_es="Banco de alimentos regional que distribuye a despensas aliadas en el centro-norte y este de WV ayudando a ciudadanos que regresan a localizar alimentos de emergencia por código postal.",
        address="484 Enterprise Drive", city="Gassaway", phone="304-364-5518", website="https://www.mountaineerfoodbank.org",
        county="Braxton", served="Barbour|Braxton|Calhoun|Clay|Doddridge|Gilmer|Harrison|Lewis|Marion|Monongalia|Pleasants|Preston|Randolph|Ritchie|Roane|Taylor|Tucker|Tyler|Upshur|Webster|Wirt|Wood", coverage="multi",
        eligibility="Open to West Virginia residents needing food assistance; partner pantry rules vary by location.",
        eligibility_es="Open to West Virginia residents needing food assistance; partner pantry rules vary by location.",
        source="https://www.mountaineerfoodbank.org")

    _mk(add, name="Facing Hunger Foodbank — Partner Pantry Network", category="food-nutrition", region="Huntington / Cabell County",
        description="Regional food bank serving the Metro Valley and southern coalfields through partner pantries, mobile distributions, and SNAP outreach for low-income families including justice-involved households.", description_es="Banco de alimentos regional que sirve al valle metropolitano y campos carboníferos del sur a través de despensas aliadas, distribuciones móviles y alcance SNAP.",
        address="1327 7th Avenue", city="Huntington", phone="304-523-6029", website="https://www.facinghunger.org",
        county="Cabell", served="Cabell|Lincoln|Logan|Mingo|Putnam|Wayne", coverage="multi",
        eligibility="Open to residents in service area; use facinghunger.org food finder for nearest pantry.",
        eligibility_es="Open to residents in service area; use facinghunger.org food finder for nearest pantry.",
        source="https://www.facinghunger.org")

    _mk(add, name="REACH Initiative — West Virginia Reentry Councils", category="reentry-organizations", region="Statewide",
        description="Statewide reentry collaborative connecting regional reentry councils, WVDCR partners, and community organizations through the REACH Initiative and wvreentry.org resource directory—a navigation hub, not a direct-service provider.", description_es="Colaboración estatal de reinserción que conecta consejos regionales, aliados WVDCR y organizaciones comunitarias a través del directorio wvreentry.org—un centro de navegación, no proveedor directo.",
        address="1409 Greenbrier Street", city="Charleston", phone="304-558-2036", website="https://www.wvreentry.org",
        county="Kanawha", served="", coverage="statewide",
        eligibility="Open to West Virginia justice-involved residents and reentry service providers seeking regional council connections.",
        eligibility_es="Open to West Virginia justice-involved residents and reentry service providers seeking regional council connections.",
        source="https://www.wvreentry.org")

    _mk(add, name="Kanawha Valley Collective — Coordinated Entry", category="housing", region="Charleston / Kanawha County",
        description="Continuum of Care coordinated entry system connecting people experiencing homelessness in the Kanawha Valley to shelter, rapid rehousing, and permanent supportive housing including returning citizens without stable housing.", description_es="Sistema de admisión coordinada del Continuum of Care conecta a personas sin hogar en el valle Kanawha con refugio, realojamiento rápido y vivienda de apoyo permanente incluidos ciudadanos que regresan.",
        address="1111 Virginia Street East", city="Charleston", phone="304-346-6355", website="https://www.kvcollective.org",
        county="Kanawha", served="Kanawha|Putnam|Boone|Clay|Lincoln|Logan", coverage="multi",
        eligibility="Adults experiencing homelessness in served counties; coordinated assessment required for housing placements.",
        eligibility_es="Adults experiencing homelessness in served counties; coordinated assessment required for housing placements.",
        source="https://www.kvcollective.org")

    _mk(add, name="The Salvation Army — Charleston Corps", category="basic-needs", region="Charleston / Kanawha County",
        description="Faith-based social services providing emergency food pantry, utility assistance, clothing, and seasonal programs for low-income Kanawha County residents including returning citizens seeking basic needs support.", description_es="Servicios sociales basados en la fe con despensa de emergencia, asistencia de servicios, ropa y programas estacionales para residentes de bajos ingresos del condado Kanawha incluidos ciudadanos que regresan.",
        address="301 Tennessee Avenue", city="Charleston", phone="304-343-4549", website="https://www.salvationarmywv.org",
        county="Kanawha", served="Kanawha", coverage="single",
        eligibility="Low-income Kanawha County residents; photo ID helpful; availability varies by program and season.",
        eligibility_es="Low-income Kanawha County residents; photo ID helpful; availability varies by program and season.",
        source="https://www.salvationarmywv.org")

    _mk(add, name="Goodwill Industries of Kanawha Valley — Workforce Center", category="employment", region="Charleston / Kanawha County",
        description="Goodwill workforce center providing job training, career coaching, skills certifications, and fair-chance employment navigation for justice-involved job seekers in the Kanawha Valley.", description_es="Centro de fuerza laboral Goodwill con capacitación laboral, coaching de carrera, certificaciones y navegación de empleo justo para buscadores de empleo con antecedentes penales en el valle Kanawha.",
        address="900 South Quarrier Street", city="Charleston", phone="304-346-0811", website="https://www.goodwillkv.org",
        county="Kanawha", served="Kanawha|Putnam|Boone|Clay|Lincoln|Logan", coverage="multi",
        eligibility="Open to job seekers including justice-involved individuals; some programs require referral partners.",
        eligibility_es="Open to job seekers including justice-involved individuals; some programs require referral partners.",
        source="https://www.goodwillkv.org")

    _mk(add, name="West Virginia Division of Motor Vehicles — ID Services", category="id-documentation", region="Statewide",
        description="West Virginia DMV issues REAL ID-compliant driver's licenses and state identification cards at regional offices statewide. Reentry partners help returning citizens gather proof of identity and residency required for employment and WV PATH benefits enrollment.", description_es="El DMV de Virginia Occidental emite licencias de conducir compatibles con REAL ID y tarjetas de identificación estatal en oficinas regionales. Los aliados de reinserción ayudan a reunir prueba de identidad y residencia.",
        address="1800 Washington Street East", city="Charleston", phone="304-926-3802", website="https://transportation.wv.gov/DMV",
        county="Kanawha", served="", coverage="statewide",
        eligibility="West Virginia residents; fees apply; bring certified birth certificate, Social Security card, and two proofs of WV residency.",
        eligibility_es="West Virginia residents; fees apply; bring certified birth certificate, Social Security card, and two proofs of WV residency.",
        source="https://transportation.wv.gov/DMV")
