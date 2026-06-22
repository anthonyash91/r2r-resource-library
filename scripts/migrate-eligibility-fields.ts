/**
 * One-time migration: split mixed `notes` into eligibility + operational notes.
 *
 * Usage:
 *   npx tsx scripts/migrate-eligibility-fields.ts
 *   npm run seed:resources
 */
import { readFileSync, writeFileSync } from "fs";
import { resolve } from "path";

const CSV_PATH = resolve(process.cwd(), "data/resources.csv");

const COLUMNS = [
  "id",
  "name",
  "category",
  "region",
  "description",
  "description_es",
  "address",
  "city",
  "phone",
  "email",
  "website",
  "eligibility",
  "eligibility_es",
  "notes",
  "notes_es",
  "hours",
  "tags",
  "services",
  "county",
] as const;

type Column = (typeof COLUMNS)[number];

const CATEGORY_ELIGIBILITY: Record<string, { en: string; es: string }> = {
  Education: {
    en: "Kentucky residents age 18 or older. All adult education and GED services are free through KYAE.",
    es: "Residentes de Kentucky de 18 años o más. Todos los servicios de educación para adultos y GED son gratuitos a través de KYAE.",
  },
  Employment: {
    en: "Open to all job seekers, including those recently released from incarceration. Core career services are free.",
    es: "Abierto a todos los buscadores de empleo, incluidos recién liberados. Los servicios básicos de carrera son gratuitos.",
  },
  Healthcare: {
    en: "Open to Kentucky residents in the service area. Medicaid, Medicare, and most insurance accepted; crisis services available regardless of ability to pay.",
    es: "Abierto a residentes de Kentucky en el área de servicio. Se acepta Medicaid, Medicare y la mayoría de seguros; servicios de crisis disponibles sin importar capacidad de pago.",
  },
  "Substance Use Treatment": {
    en: "Adults seeking substance use treatment. Medicaid and private insurance accepted at many locations; call for intake and admission criteria.",
    es: "Adultos que buscan tratamiento de sustancias. Se acepta Medicaid y seguro privado en muchas ubicaciones; llame para criterios de admisión.",
  },
  Housing: {
    en: "Varies by program—many accept individuals with felony records. Most transitional and reentry housing requires referral or application; call to confirm bed availability and criteria.",
    es: "Varía según el programa—muchos aceptan personas con antecedentes penales. La mayoría de vivienda transitoria requiere referido o solicitud; llame para confirmar disponibilidad.",
  },
  "Legal Aid": {
    en: "Low-income Kentucky residents. Intake required to confirm income eligibility and whether your legal issue is covered.",
    es: "Residentes de Kentucky de bajos ingresos. Se requiere admisión para confirmar elegibilidad de ingresos y si su caso legal está cubierto.",
  },
  "Food & Nutrition": {
    en: "Varies by program—many serve low-income households; some pantries are open to all. Income verification may apply for benefits programs.",
    es: "Varía según el programa—muchos sirven hogares de bajos ingresos; algunas despensas están abiertas a todos. Puede aplicar verificación de ingresos.",
  },
  "Financial Assistance": {
    en: "Low-income individuals and families; income guidelines apply for most programs. Criminal history is generally not a barrier.",
    es: "Personas y familias de bajos ingresos; aplican límites de ingresos en la mayoría de programas. El historial criminal generalmente no es barrera.",
  },
  "ID & Documentation": {
    en: "Kentucky residents. Returning citizens with felony convictions may use a Felon Release Letter plus certified birth certificate for a standard ID—see program details.",
    es: "Residentes de Kentucky. Ciudadanos que regresan con condenas previas pueden usar Carta de Liberación más acta de nacimiento certificada para ID estándar.",
  },
  Transportation: {
    en: "Open to the public; reduced fares may require eligibility documentation (age, disability, or income).",
    es: "Abierto al público; tarifas reducidas pueden requerir documentación de elegibilidad (edad, discapacidad o ingresos).",
  },
  "Family & Children": {
    en: "Varies by program—open to parents, caregivers, and families affected by incarceration.",
    es: "Varía según el programa—abierto a padres, cuidadores y familias afectadas por encarcelamiento.",
  },
  "Peer Support": {
    en: "Open to adults in recovery or seeking peer support, including those recently released from incarceration.",
    es: "Abierto a adultos en recuperación o que buscan apoyo entre pares, incluidos recién liberados.",
  },
  Veterans: {
    en: "U.S. military veterans and eligible family members. Some programs serve veterans with justice involvement.",
    es: "Veteranos militares de EE.UU. y familiares elegibles. Algunos programas atienden veteranos con participación en justicia penal.",
  },
  "Basic Needs": {
    en: "Low-income individuals and families; program-specific income guidelines apply. Open regardless of criminal history at most community action agencies.",
    es: "Personas y familias de bajos ingresos; aplican límites según programa. Abierto sin importar historial criminal en la mayoría de agencias comunitarias.",
  },
  "Probation & Parole": {
    en: "Individuals on felony probation, parole, or conditional discharge supervised by Kentucky DOC in the listed district.",
    es: "Personas en libertad condicional, supervisada o descarga condicional por delitos graves bajo supervisión del DOC de Kentucky.",
  },
  "Reentry Organizations": {
    en: "Justice-involved individuals reintegrating from incarceration and community partners; program-specific enrollment applies.",
    es: "Personas involucradas con la justicia reintegrándose desde la cárcel y socios comunitarios; aplica inscripción según programa.",
  },
  "State Agency": {
    en: "Varies by program—generally serves Kentucky residents under DOC custody, supervision, or seeking state reentry services.",
    es: "Varía según el programa—generalmente sirve a residentes de Kentucky bajo custodia DOC, supervisión o que buscan servicios estatales de reintegración.",
  },
};

const ELIGIBILITY_PATTERNS = [
  /\breferral required\b/i,
  /\bcannot self-enroll\b/i,
  /\blow-income\b/i,
  /\bincome (guidelines|eligibility|verification|limit|up to)\b/i,
  /\beligib(le|ility)\b/i,
  /\bmust (meet|have|be|submit|complete)\b/i,
  /\brequires?\b/i,
  /\bopen to all\b/i,
  /\bregardless of criminal\b/i,
  /\bfelony[- ]friendly\b/i,
  /\baccepts residents with felony\b/i,
  /\bDOC inmates?\b/i,
  /\bstate inmates?\b/i,
  /\bstate-sentenced\b/i,
  /\bprobation\b/i,
  /\bparole\b/i,
  /\bages? 18\b/i,
  /\b18\+\b/,
  /\bKentucky residents?\b/i,
  /\b\d+% FPL\b/i,
  /\bverification (required|may apply)\b/i,
  /\bMedicaid (and|,) (Medicare|most insurance)\b/i,
  /\bsliding scale\b/i,
  /\bautomatic restoration\b/i,
  /\bKRS \d+/i,
  /\bdrug felony ban\b/i,
  /\binstitutional referral\b/i,
  /\bcommunity custody\b/i,
  /\bunder (DOC )?supervision\b/i,
  /\bjustice-involved\b/i,
  /\bfree to Kentucky\b/i,
  /\ball services (are )?free\b/i,
  /\buninsured\b/i,
  /\bunderinsured\b/i,
  /\bopen enrollment\b/i,
  /\bintake required\b/i,
  /\bincome guidelines\b/i,
  /\bfelony records?\b/i,
  /\brecently released\b/i,
  /\breintegrating from incarceration\b/i,
  /\bFelon Release Letter\b/i,
  /\bKTAP recipients\b/i,
  /\bfirst-time GED\b/i,
  /\bwaived for eligible\b/i,
  /\bno (proof of income|questions asked)\b/i,
  /\banyone in crisis\b/i,
  /\bwithout regard to (criminal|faith)\b/i,
  /\bno cost\b/i,
  /\bno income limit\b/i,
  /\bU\.S\. (military )?veterans?\b/i,
  /\bnon-violent\b/i,
  /\bviolent felon(y|ies)\b/i,
  /\bnot open to the public\b/i,
  /\brequires DOC classification\b/i,
  /\bnot a barrier\b/i,
  // Spanish
  /\breferido requerido\b/i,
  /\bno puede auto-inscribirse\b/i,
  /\bbajos ingresos\b/i,
  /\belegib(le|ilidad)\b/i,
  /\babierto a todos\b/i,
  /\bsin importar el historial criminal\b/i,
  /\bantecedentes penales\b/i,
  /\breclusos estatales\b/i,
  /\blibertad condicional\b/i,
  /\bresidentes de Kentucky\b/i,
  /\binvolucradas? con la justicia\b/i,
  /\brecién liberad[oa]s?\b/i,
  /\bse requiere admisión\b/i,
  /\btodos los servicios.*gratuitos\b/i,
  /\bveteranos\b/i,
  /\bno abierto al público\b/i,
  /\brequiere clasificación DOC\b/i,
];

const OPERATIONAL_PATTERNS = [
  /\bAlso serves\b/i,
  /\bTambién sirve\b/i,
  /\bServes Anderson,/i,
  /\bSirve los condados\b/i,
  /\bcounties including\b/i,
  /\bcondados del\b/i,
  /\bvia appointment\b/i,
  /\bcon cita\b/i,
  /\bAlternate (line|location|phone)\b/i,
  /\bLínea alternativa\b/i,
  /\bCrisis[:/]/i,
  /\bCrisis 24/i,
  /\bFax\b/i,
  /\b@\w+\./,
  /\bhttps?:\/\//i,
  /\b\.(gov|org|com|ky\.gov)\b/i,
  /\b\d{3}[-.)]\d{3}[-.)]\d{4}\b/,
  /\b1-\d{3}-\d{3}-\d{4}\b/,
  /\bPromo code\b/i,
  /\bCódigo promocional\b/i,
  /\bco-located\b/i,
  /\bPartner(s)? include\b/i,
  /\bAliados incluyen\b/i,
  /\borientation\b/i,
  /\borientación\b/i,
  /\bHotline\b/i,
  /\bLínea (24|de crisis)\b/i,
  /\bschedule (at|through|appointments)\b/i,
  /\bWalk-in intakes\b/i,
  /\bintakes sin cita\b/i,
  /\bDrop box\b/i,
  /\bMail (applications|payments)\b/i,
  /\bEnter via\b/i,
  /\bEntrada por\b/i,
  /\bsatellite\b/i,
  /\bcheck (website|pantry|.*\.org)\b/i,
  /\bconsulte\b/i,
  /\bregistration opens\b/i,
  /\bclinic dates vary\b/i,
  /\bseasonal\b/i,
  /\bestacional\b/i,
  /\bappointment phone\b/i,
  /\bNational toll-free\b/i,
  /\bDoes not provide direct\b/i,
  /\bnetworking council\b/i,
  /\bvirtual (appointments|classes)\b/i,
  /\btelehealth\b/i,
  /\bfirst Tuesday\b/i,
  /\bpr(i|í)mer martes\b/i,
  /\bOffice mailing\b/i,
  /\bCorreo:\b/i,
  /\bPO Box\b/i,
  /\bSede:\b/i,
  /\bParking\b/i,
  /\bMyTARC\b/i,
  /\bAfter-hours\b/i,
  /\bPayment window\b/i,
  /\bLost & found\b/i,
  /\bVitalChek\b/i,
  /\btext zip\b/i,
  /\bDCBS Call\b/i,
  /\bFor unemployment claims\b/i,
  /\bsee \w+\.(org|gov)\b/i,
  /\bvisit \w+\./i,
  /\bMon–|Monday–|Martes|Lunes–/i,
  /\bextended hours\b/i,
  /\bhorario extendido\b/i,
  /\bTTY\b/i,
  /\bNeighborhood Center hours\b/i,
  /\bPrestonsburg campus\b/i,
  /\bCampus Prestonsburg\b/i,
  /\bKynector\b/i,
  /\bLIHEAP (enrollment|seasonal)\b/i,
  /\bApply (online|at any)\b/i,
  /\bSame kynect portal\b/i,
  /\bDial 2-1-1\b/i,
  /\bMultiple (county|office)\b/i,
  /\bMúltiples oficinas\b/i,
  /\bVerify (county|office)\b/i,
  /\bVerifique oficina\b/i,
];

function parseCsv(content: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let field = "";
  let inQuotes = false;

  for (let i = 0; i < content.length; i++) {
    const char = content[i];
    const next = content[i + 1];

    if (inQuotes) {
      if (char === '"' && next === '"') {
        field += '"';
        i++;
      } else if (char === '"') {
        inQuotes = false;
      } else {
        field += char;
      }
      continue;
    }

    if (char === '"') {
      inQuotes = true;
    } else if (char === ",") {
      row.push(field);
      field = "";
    } else if (char === "\n" || (char === "\r" && next === "\n")) {
      row.push(field);
      if (row.some((cell) => cell.trim())) rows.push(row);
      row = [];
      field = "";
      if (char === "\r") i++;
    } else if (char !== "\r") {
      field += char;
    }
  }

  if (field.length > 0 || row.length > 0) {
    row.push(field);
    if (row.some((cell) => cell.trim())) rows.push(row);
  }

  return rows;
}

function escapeCsvField(value: string) {
  if (/[",\n\r]/.test(value)) {
    return `"${value.replace(/"/g, '""')}"`;
  }
  return value;
}

function serializeCsv(rows: string[][]) {
  return rows.map((row) => row.map(escapeCsvField).join(",")).join("\n") + "\n";
}

function splitSentences(text: string): string[] {
  if (!text.trim()) return [];
  return text
    .split(/(?<=[.!?])\s+|\s*;\s+/)
    .map((s) => s.trim())
    .filter(Boolean);
}

function scorePatterns(text: string, patterns: RegExp[]): number {
  return patterns.reduce((score, pattern) => (pattern.test(text) ? score + 1 : score), 0);
}

function classifySentence(sentence: string): "eligibility" | "operational" | "unknown" {
  const eScore = scorePatterns(sentence, ELIGIBILITY_PATTERNS);
  const oScore = scorePatterns(sentence, OPERATIONAL_PATTERNS);

  if (eScore > oScore) return "eligibility";
  if (oScore > eScore) return "operational";
  return "unknown";
}

function splitField(text: string): { eligibility: string[]; notes: string[] } {
  const eligibility: string[] = [];
  const notes: string[] = [];

  for (const sentence of splitSentences(text)) {
    const kind = classifySentence(sentence);
    if (kind === "eligibility") eligibility.push(sentence);
    else if (kind === "operational") notes.push(sentence);
    else {
      // Short contact-only fragments → operational; otherwise eligibility if it describes who
      if (/^\(?\d/.test(sentence) || sentence.length < 40) {
        notes.push(sentence);
      } else if (
        /\b(for|serve[sd]?|atiende|sirve)\b/i.test(sentence) &&
        !/\b(counties|condados)\b/i.test(sentence)
      ) {
        eligibility.push(sentence);
      } else {
        notes.push(sentence);
      }
    }
  }

  return { eligibility, notes };
}

function extractFromDescription(description: string): string[] {
  const found: string[] = [];
  for (const sentence of splitSentences(description)) {
    if (scorePatterns(sentence, ELIGIBILITY_PATTERNS) >= 2) {
      found.push(sentence);
    }
  }
  return found.slice(0, 2);
}

function dedupeJoin(parts: string[]): string {
  const seen = new Set<string>();
  const out: string[] = [];
  for (const part of parts) {
    const key = part.trim().toLowerCase();
    if (!key || seen.has(key)) continue;
    seen.add(key);
    out.push(part.trim());
  }
  return out.join(" ");
}

function migrateRow(record: Record<string, string>) {
  const category = record.category?.trim() ?? "";
  const defaults = CATEGORY_ELIGIBILITY[category];

  const enSplit = splitField(record.notes ?? "");
  const esSplit = splitField(record.notes_es ?? "");

  let eligibility = dedupeJoin(enSplit.eligibility);
  let eligibilityEs = dedupeJoin(esSplit.eligibility);
  let notes = dedupeJoin(enSplit.notes);
  let notesEs = dedupeJoin(esSplit.notes);

  if (!eligibility) {
    const fromDesc = extractFromDescription(record.description ?? "");
    eligibility = dedupeJoin(fromDesc);
  }

  if (!eligibility && defaults) {
    eligibility = defaults.en;
  }

  if (!eligibilityEs && defaults) {
    eligibilityEs = defaults.es;
  }

  // If notes ended empty but original had content classified as eligibility-only, keep operational hints from description untouched
  if (!notes && record.notes?.trim() && enSplit.eligibility.length === splitSentences(record.notes).length) {
    notes = "";
  }

  return {
    ...record,
    eligibility,
    eligibility_es: eligibilityEs,
    notes,
    notes_es: notesEs,
  };
}

const raw = readFileSync(CSV_PATH, "utf8");
const rows = parseCsv(raw);
const oldHeader = rows[0].map((h) => h.trim().toLowerCase());

const records = rows.slice(1).map((values) => {
  const record: Record<string, string> = {};
  oldHeader.forEach((key, index) => {
    record[key] = values[index] ?? "";
  });
  return record;
});

const migrated = records.map(migrateRow);

const outRows: string[][] = [Array.from(COLUMNS)];
for (const record of migrated) {
  outRows.push(COLUMNS.map((col) => record[col] ?? ""));
}

writeFileSync(CSV_PATH, serializeCsv(outRows));

const stats = {
  withEligibility: migrated.filter((r) => r.eligibility?.trim()).length,
  withNotes: migrated.filter((r) => r.notes?.trim()).length,
  withEligibilityEs: migrated.filter((r) => r.eligibility_es?.trim()).length,
};

console.log(`Migrated ${migrated.length} resources in ${CSV_PATH}`);
console.log(`  eligibility filled: ${stats.withEligibility}/${migrated.length}`);
console.log(`  notes (operational) filled: ${stats.withNotes}/${migrated.length}`);
console.log(`  eligibility_es filled: ${stats.withEligibilityEs}/${migrated.length}`);
console.log("\nNext: npm run seed:resources → run migrations + supabase/seed-resources.sql");
