import type { Resource } from "@/types";
import { MOCK_CATEGORIES } from "./mock-data-categories";

const now = Date.now();
const nowIso = new Date(now).toISOString();

interface Location {
  state: string;
  county: string;
  city: string;
  latitude: number;
  longitude: number;
  zip: string;
}

const US_LOCATIONS: Location[] = [
  { state: "California", county: "Los Angeles", city: "Los Angeles", latitude: 34.0522, longitude: -118.2437, zip: "90012" },
  { state: "California", county: "San Francisco", city: "San Francisco", latitude: 37.7749, longitude: -122.4194, zip: "94102" },
  { state: "California", county: "San Diego", city: "San Diego", latitude: 32.7157, longitude: -117.1611, zip: "92101" },
  { state: "California", county: "Sacramento", city: "Sacramento", latitude: 38.5816, longitude: -121.4944, zip: "95814" },
  { state: "Texas", county: "Harris", city: "Houston", latitude: 29.7604, longitude: -95.3698, zip: "77002" },
  { state: "Texas", county: "Dallas", city: "Dallas", latitude: 32.7767, longitude: -96.797, zip: "75201" },
  { state: "Texas", county: "Travis", city: "Austin", latitude: 30.2672, longitude: -97.7431, zip: "78701" },
  { state: "Texas", county: "Bexar", city: "San Antonio", latitude: 29.4241, longitude: -98.4936, zip: "78205" },
  { state: "New York", county: "New York", city: "New York", latitude: 40.7128, longitude: -74.006, zip: "10001" },
  { state: "New York", county: "Kings", city: "Brooklyn", latitude: 40.6782, longitude: -73.9442, zip: "11201" },
  { state: "New York", county: "Erie", city: "Buffalo", latitude: 42.8864, longitude: -78.8784, zip: "14202" },
  { state: "Florida", county: "Miami-Dade", city: "Miami", latitude: 25.7617, longitude: -80.1918, zip: "33130" },
  { state: "Florida", county: "Orange", city: "Orlando", latitude: 28.5383, longitude: -81.3792, zip: "32801" },
  { state: "Florida", county: "Hillsborough", city: "Tampa", latitude: 27.9506, longitude: -82.4572, zip: "33602" },
  { state: "Illinois", county: "Cook", city: "Chicago", latitude: 41.8781, longitude: -87.6298, zip: "60601" },
  { state: "Pennsylvania", county: "Philadelphia", city: "Philadelphia", latitude: 39.9526, longitude: -75.1652, zip: "19107" },
  { state: "Pennsylvania", county: "Allegheny", city: "Pittsburgh", latitude: 40.4406, longitude: -79.9959, zip: "15222" },
  { state: "Ohio", county: "Franklin", city: "Columbus", latitude: 39.9612, longitude: -82.9988, zip: "43215" },
  { state: "Ohio", county: "Cuyahoga", city: "Cleveland", latitude: 41.4993, longitude: -81.6944, zip: "44114" },
  { state: "Georgia", county: "Fulton", city: "Atlanta", latitude: 33.749, longitude: -84.388, zip: "30303" },
  { state: "North Carolina", county: "Mecklenburg", city: "Charlotte", latitude: 35.2271, longitude: -80.8431, zip: "28202" },
  { state: "North Carolina", county: "Wake", city: "Raleigh", latitude: 35.7796, longitude: -78.6382, zip: "27601" },
  { state: "Michigan", county: "Wayne", city: "Detroit", latitude: 42.3314, longitude: -83.0458, zip: "48226" },
  { state: "Arizona", county: "Maricopa", city: "Phoenix", latitude: 33.4484, longitude: -112.074, zip: "85004" },
  { state: "Washington", county: "King", city: "Seattle", latitude: 47.6062, longitude: -122.3321, zip: "98101" },
  { state: "Colorado", county: "Denver", city: "Denver", latitude: 39.7392, longitude: -104.9903, zip: "80202" },
  { state: "Massachusetts", county: "Suffolk", city: "Boston", latitude: 42.3601, longitude: -71.0589, zip: "02108" },
  { state: "Virginia", county: "Richmond City", city: "Richmond", latitude: 37.5407, longitude: -77.436, zip: "23219" },
  { state: "Tennessee", county: "Davidson", city: "Nashville", latitude: 36.1627, longitude: -86.7816, zip: "37219" },
  { state: "Maryland", county: "Baltimore City", city: "Baltimore", latitude: 39.2904, longitude: -76.6122, zip: "21201" },
  { state: "Minnesota", county: "Hennepin", city: "Minneapolis", latitude: 44.9778, longitude: -93.265, zip: "55401" },
  { state: "Missouri", county: "Jackson", city: "Kansas City", latitude: 39.0997, longitude: -94.5786, zip: "64106" },
  { state: "Oregon", county: "Multnomah", city: "Portland", latitude: 45.5152, longitude: -122.6784, zip: "97204" },
  { state: "Nevada", county: "Clark", city: "Las Vegas", latitude: 36.1699, longitude: -115.1398, zip: "89101" },
  { state: "Wisconsin", county: "Milwaukee", city: "Milwaukee", latitude: 43.0389, longitude: -87.9065, zip: "53202" },
  { state: "Indiana", county: "Marion", city: "Indianapolis", latitude: 39.7684, longitude: -86.1581, zip: "46204" },
  { state: "Alabama", county: "Jefferson", city: "Birmingham", latitude: 33.5207, longitude: -86.8025, zip: "35203" },
  { state: "Louisiana", county: "Orleans", city: "New Orleans", latitude: 29.9511, longitude: -90.0715, zip: "70112" },
  { state: "Kentucky", county: "Jefferson", city: "Louisville", latitude: 38.2527, longitude: -85.7585, zip: "40202" },
  { state: "Oklahoma", county: "Oklahoma", city: "Oklahoma City", latitude: 35.4676, longitude: -97.5164, zip: "73102" },
  { state: "Connecticut", county: "Hartford", city: "Hartford", latitude: 41.7658, longitude: -72.6734, zip: "06103" },
  { state: "Utah", county: "Salt Lake", city: "Salt Lake City", latitude: 40.7608, longitude: -111.891, zip: "84101" },
  { state: "Iowa", county: "Polk", city: "Des Moines", latitude: 41.5868, longitude: -93.625, zip: "50309" },
  { state: "Arkansas", county: "Pulaski", city: "Little Rock", latitude: 34.7465, longitude: -92.2896, zip: "72201" },
  { state: "Kansas", county: "Sedgwick", city: "Wichita", latitude: 37.6872, longitude: -97.3301, zip: "67202" },
  { state: "New Mexico", county: "Bernalillo", city: "Albuquerque", latitude: 35.0844, longitude: -106.6504, zip: "87102" },
  { state: "Nebraska", county: "Douglas", city: "Omaha", latitude: 41.2565, longitude: -95.9345, zip: "68102" },
  { state: "South Carolina", county: "Richland", city: "Columbia", latitude: 34.0007, longitude: -81.0348, zip: "29201" },
  { state: "Mississippi", county: "Hinds", city: "Jackson", latitude: 32.2988, longitude: -90.1848, zip: "39201" },
  { state: "Hawaii", county: "Honolulu", city: "Honolulu", latitude: 21.3069, longitude: -157.8583, zip: "96813" },
  { state: "Alaska", county: "Anchorage", city: "Anchorage", latitude: 61.2181, longitude: -149.9003, zip: "99501" },
  { state: "Delaware", county: "New Castle", city: "Wilmington", latitude: 39.7391, longitude: -75.5398, zip: "19801" },
  { state: "Rhode Island", county: "Providence", city: "Providence", latitude: 41.824, longitude: -71.4128, zip: "02903" },
  { state: "Maine", county: "Cumberland", city: "Portland", latitude: 43.6591, longitude: -70.2568, zip: "04101" },
  { state: "Montana", county: "Yellowstone", city: "Billings", latitude: 45.7833, longitude: -108.5007, zip: "59101" },
  { state: "Idaho", county: "Ada", city: "Boise", latitude: 43.615, longitude: -116.2023, zip: "83702" },
  { state: "West Virginia", county: "Kanawha", city: "Charleston", latitude: 38.3498, longitude: -81.6326, zip: "25301" },
  { state: "New Hampshire", county: "Hillsborough", city: "Manchester", latitude: 42.9956, longitude: -71.4548, zip: "03101" },
  { state: "Wyoming", county: "Laramie", city: "Cheyenne", latitude: 41.14, longitude: -104.8202, zip: "82001" },
];

interface CategoryTemplate {
  categoryId: string;
  namePrefixes: string[];
  description: string;
  services: string[];
  tags: string[];
  eligibility: string;
}

const CATEGORY_TEMPLATES: CategoryTemplate[] = [
  {
    categoryId: "cat-housing",
    namePrefixes: ["Second Chance Housing", "Transitional Living Center", "Safe Harbor Shelter", "New Start Housing", "Bridge Home Program", "Hope House"],
    description: "Transitional and supportive housing for individuals returning to the community. Case managers help with housing plans, landlord referrals, and life skills.",
    services: ["Transitional housing", "Case management", "Rental assistance", "Landlord referrals"],
    tags: ["housing", "transitional", "shelter"],
    eligibility: "Recently released or at risk of homelessness. Ages 18+.",
  },
  {
    categoryId: "cat-employment",
    namePrefixes: ["Reentry Works", "Job Ready Center", "Second Chance Employment", "Career Bridge Program", "Fresh Start Jobs", "WorkForce Reentry"],
    description: "Job training, resume help, and placement services for people with criminal records. Connects you with fair-chance employers in your area.",
    services: ["Job training", "Resume help", "Interview coaching", "Job placement", "Work clothing"],
    tags: ["employment", "jobs", "training"],
    eligibility: "Open to all. Priority for recently released individuals.",
  },
  {
    categoryId: "cat-food",
    namePrefixes: ["Community Food Pantry", "Neighborhood Food Bank", "Meals & More", "Harvest Hope Kitchen", "Open Door Food Program", "Daily Bread Center"],
    description: "Free groceries, hot meals, and help enrolling in SNAP benefits. No ID required at most locations.",
    services: ["Free groceries", "Hot meals", "SNAP enrollment help", "Nutrition education"],
    tags: ["food", "SNAP", "meals"],
    eligibility: "Open to everyone. No proof of income required.",
  },
  {
    categoryId: "cat-healthcare",
    namePrefixes: ["Community Health Clinic", "Free Care Center", "Neighborhood Medical Clinic", "Wellness Access Program", "Open Door Health", "Care For All Clinic"],
    description: "Free or low-cost medical, dental, and vision care. Prescription assistance and referrals to specialists when needed.",
    services: ["Primary care", "Dental care", "Vision care", "Prescription assistance"],
    tags: ["healthcare", "clinic", "medical"],
    eligibility: "Uninsured or underinsured adults.",
  },
  {
    categoryId: "cat-mental-health",
    namePrefixes: ["Pathways Counseling", "Mindful Recovery Center", "Community Therapy Services", "Healing Hearts Clinic", "Wellness & Recovery", "Hope Counseling Center"],
    description: "Counseling and therapy for anxiety, depression, trauma, and reentry adjustment. Individual and group sessions available.",
    services: ["Individual therapy", "Group therapy", "Crisis counseling", "Telehealth"],
    tags: ["mental health", "therapy", "counseling"],
    eligibility: "Adults 18+. Sliding scale and Medicaid accepted.",
  },
  {
    categoryId: "cat-recovery",
    namePrefixes: ["New Beginnings Recovery", "Clean Slate Program", "Recovery Path Center", "Serenity House", "Turning Point Recovery", "Bridge to Sobriety"],
    description: "Substance abuse treatment, support groups, and sober living referrals. Peer specialists who understand the reentry journey.",
    services: ["Outpatient treatment", "Support groups", "Sober living referrals", "Peer support"],
    tags: ["recovery", "substance abuse", "sober living"],
    eligibility: "Adults seeking recovery support.",
  },
  {
    categoryId: "cat-transportation",
    namePrefixes: ["Transit Access Program", "Ride to Work Initiative", "Mobility Assistance Center", "Community Transit Help", "Bus Pass Program", "Getting There Center"],
    description: "Free or reduced bus passes and help planning routes to jobs, appointments, and services.",
    services: ["Free bus passes", "Reduced fare cards", "Route planning help", "Rides to interviews"],
    tags: ["transportation", "bus passes", "transit"],
    eligibility: "Recently released or enrolled in a reentry program.",
  },
  {
    categoryId: "cat-education",
    namePrefixes: ["Adult Learning Center", "GED Success Program", "Skills for Life Academy", "Second Chance Education", "Career Training Institute", "Learning Bridge Center"],
    description: "GED preparation, adult literacy, vocational training, and computer skills classes.",
    services: ["GED prep", "Adult literacy", "Vocational training", "Computer skills"],
    tags: ["education", "GED", "training"],
    eligibility: "Adults 18 and older. Open enrollment.",
  },
  {
    categoryId: "cat-financial",
    namePrefixes: ["Financial Empowerment Center", "Money Matters Program", "Budget & Build Workshop", "Economic Opportunity Center", "Fresh Start Finance", "Community Credit Help"],
    description: "Financial coaching, bank account setup, budgeting workshops, and emergency assistance for basic needs.",
    services: ["Financial coaching", "Bank account help", "Budgeting workshops", "Emergency assistance"],
    tags: ["financial", "budgeting", "benefits"],
    eligibility: "Low-income individuals.",
  },
  {
    categoryId: "cat-legal",
    namePrefixes: ["Legal Aid Reentry Clinic", "Justice Access Project", "Record Relief Center", "Fair Chance Legal Help", "Rights Restoration Clinic", "Community Legal Services"],
    description: "Free legal help with expungement, license restoration, housing discrimination, and benefits appeals.",
    services: ["Record expungement", "License restoration", "Legal clinics", "Benefits appeals"],
    tags: ["legal", "expungement", "legal aid"],
    eligibility: "Low-income individuals. Income verification may apply.",
  },
  {
    categoryId: "cat-id",
    namePrefixes: ["ID Recovery Program", "Document Assistance Center", "Identity Restoration Help", "Paperwork Plus", "Fresh Start ID Services", "Vital Records Help Desk"],
    description: "Help obtaining birth certificates, state IDs, Social Security cards, and other documents needed for work and housing.",
    services: ["Birth certificate help", "State ID assistance", "Social Security card help", "Fee waivers"],
    tags: ["ID", "documents", "vital records"],
    eligibility: "Recently released or homeless individuals.",
  },
  {
    categoryId: "cat-family",
    namePrefixes: ["Family Reunification Services", "Parenting Path Program", "Families Together Center", "Homecoming Family Support", "Reconnect Program", "Strong Families Initiative"],
    description: "Support rebuilding family relationships after incarceration. Parenting classes, counseling, and visitation help.",
    services: ["Parenting classes", "Family counseling", "Visitation support", "Co-parenting help"],
    tags: ["family", "parenting", "reunification"],
    eligibility: "Parents and family members affected by incarceration.",
  },
  {
    categoryId: "cat-veterans",
    namePrefixes: ["Veterans Reentry Center", "Heroes Homecoming Program", "Vet Support Services", "Operation Second Chance", "Veterans Resource Hub", "Served & Supported"],
    description: "VA benefits enrollment, housing vouchers, employment programs, and peer mentoring for veterans.",
    services: ["VA benefits help", "Housing vouchers", "Employment programs", "Peer mentoring"],
    tags: ["veterans", "VA benefits", "military"],
    eligibility: "Veterans with criminal justice involvement.",
  },
  {
    categoryId: "cat-disability",
    namePrefixes: ["Disability Rights Center", "Access For All Program", "Ability Resource Hub", "Independent Living Center", "Disability Benefits Help", "Inclusive Support Services"],
    description: "Help applying for disability benefits, accessibility accommodations, and assistive technology.",
    services: ["Benefits application help", "Accessibility advocacy", "Assistive technology", "Independent living skills"],
    tags: ["disability", "benefits", "accessibility"],
    eligibility: "Individuals with disabilities seeking support.",
  },
  {
    categoryId: "cat-community",
    namePrefixes: ["Community Bridge Program", "Peer Support Network", "Reentry Circle", "Neighbor to Neighbor", "Together We Rise Center", "Community Connection Hub"],
    description: "Peer mentoring, support groups, and community activities for people rebuilding their lives.",
    services: ["Peer mentoring", "Support groups", "Community events", "Resource navigation"],
    tags: ["community", "mentoring", "peer support"],
    eligibility: "Open to all formerly incarcerated individuals.",
  },
  {
    categoryId: "cat-emergency",
    namePrefixes: ["Crisis Response Center", "Emergency Assistance Line", "Immediate Help Hotline", "Safe Haven Emergency", "24/7 Crisis Support", "Urgent Care Shelter"],
    description: "24/7 crisis hotline, emergency shelter, meals, and immediate connection to long-term resources.",
    services: ["Crisis hotline", "Emergency shelter", "Meals", "Resource referrals"],
    tags: ["emergency", "crisis", "24/7"],
    eligibility: "Anyone in crisis. No questions asked for emergency shelter.",
  },
];

const STATE_ABBR: Record<string, string> = {
  California: "CA", Texas: "TX", "New York": "NY", Florida: "FL", Illinois: "IL",
  Pennsylvania: "PA", Ohio: "OH", Georgia: "GA", "North Carolina": "NC", Michigan: "MI",
  Arizona: "AZ", Washington: "WA", Colorado: "CO", Massachusetts: "MA", Virginia: "VA",
  Tennessee: "TN", Maryland: "MD", Minnesota: "MN", Missouri: "MO", Oregon: "OR",
  Nevada: "NV", Wisconsin: "WI", Indiana: "IN", Alabama: "AL", Louisiana: "LA",
  Kentucky: "KY", Oklahoma: "OK", Connecticut: "CT", Utah: "UT", Iowa: "IA",
  Arkansas: "AR", Kansas: "KS", "New Mexico": "NM", Nebraska: "NE", "South Carolina": "SC",
  Mississippi: "MS", Hawaii: "HI", Alaska: "AK", Delaware: "DE", "Rhode Island": "RI",
  Maine: "ME", Montana: "MT", Idaho: "ID", "West Virginia": "WV", "New Hampshire": "NH",
  Wyoming: "WY",
};

function withCategory(
  resource: Omit<Resource, "category">,
  categories: typeof MOCK_CATEGORIES
): Resource {
  const category = categories.find((c) => c.id === resource.category_id);
  return { ...resource, category };
}

export function generateMockResources(categories: typeof MOCK_CATEGORIES): Resource[] {
  const resources: Resource[] = [];
  const total = 100;

  for (let i = 0; i < total; i++) {
    const template = CATEGORY_TEMPLATES[i % CATEGORY_TEMPLATES.length];
    const location = US_LOCATIONS[i % US_LOCATIONS.length];
    const namePrefix = template.namePrefixes[i % template.namePrefixes.length];
    const suffix = i >= CATEGORY_TEMPLATES.length ? ` – ${location.city}` : ` – ${location.city}`;
    const name = `${namePrefix}${suffix}`;
    const daysAgo = (i * 3) % 90;
    const createdAt = new Date(now - daysAgo * 86400000).toISOString();
    const abbr = STATE_ABBR[location.state] ?? "US";
    const streetNum = 100 + (i * 17) % 8900;
    const areaCode = [213, 310, 713, 718, 312, 404, 602, 206, 303, 617, 215, 502, 505, 808][i % 13];
    const phone = `${areaCode}555${String(1000 + (i % 9000)).padStart(4, "0")}`;

    resources.push(
      withCategory(
        {
          id: `res-${i + 1}`,
          name,
          category_id: template.categoryId,
          description: `${template.description} Serving ${location.city}, ${location.state} and surrounding communities.`,
          state: location.state,
          county: location.county,
          city: location.city,
          address: `${streetNum} Community Way, ${location.city}, ${abbr} ${location.zip}`,
          phone,
          website: `https://example.org/resource/${i + 1}`,
          email: i % 4 === 0 ? null : `help${i + 1}@example.org`,
          hours:
            template.categoryId === "cat-emergency"
              ? "24 hours a day, 7 days a week"
              : "Monday–Friday, 8:00 AM – 5:00 PM",
          eligibility: template.eligibility,
          services: template.services,
          tags: [...template.tags, location.city.toLowerCase().replace(/\s+/g, "-")],
          latitude: location.latitude + (i % 10) * 0.002,
          longitude: location.longitude - (i % 10) * 0.002,
          is_featured: i < 3,
          status: "active",
          view_count: 50 + ((i * 37) % 500),
          save_count: 10 + ((i * 13) % 120),
          created_at: createdAt,
          updated_at: nowIso,
          created_by: null,
        },
        categories
      )
    );
  }

  return resources;
}
