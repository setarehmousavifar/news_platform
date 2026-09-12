"""Premium English news catalog for seed_premium management command."""

from __future__ import annotations

CATEGORY_NAMES = [
    'breaking_news',
    'world',
    'politics',
    'business',
    'economy',
    'technology',
    'science',
    'health',
    'sports',
    'entertainment',
    'culture',
    'lifestyle',
    'opinion',
    'education',
    'environment',
    'crime',
    'travel',
    'food',
    'real_estate',
    'weather',
    'video',
]

AUTHORS = [
    {
        'key': 'sarah_chen',
        'username': 'sarah_chen',
        'email': 'sarah.chen@nevox.news',
        'phone': '09121110001',
        'first_name': 'Sarah',
        'last_name': 'Chen',
    },
    {
        'key': 'marcus_webb',
        'username': 'marcus_webb',
        'email': 'marcus.webb@nevox.news',
        'phone': '09121110002',
        'first_name': 'Marcus',
        'last_name': 'Webb',
    },
    {
        'key': 'elena_rodriguez',
        'username': 'elena_rodriguez',
        'email': 'elena.rodriguez@nevox.news',
        'phone': '09121110003',
        'first_name': 'Elena',
        'last_name': 'Rodriguez',
    },
    {
        'key': 'james_okonkwo',
        'username': 'james_okonkwo',
        'email': 'james.okonkwo@nevox.news',
        'phone': '09121110004',
        'first_name': 'James',
        'last_name': 'Okonkwo',
    },
    {
        'key': 'priya_sharma',
        'username': 'priya_sharma',
        'email': 'priya.sharma@nevox.news',
        'phone': '09121110005',
        'first_name': 'Priya',
        'last_name': 'Sharma',
    },
    {
        'key': 'david_falk',
        'username': 'david_falk',
        'email': 'david.falk@nevox.news',
        'phone': '09121110006',
        'first_name': 'David',
        'last_name': 'Falk',
    },
]

_AUTHOR_KEYS = [a['key'] for a in AUTHORS]


def _article(
    category: str,
    title: str,
    lead: str,
    paragraphs: list[str],
    tags: list[str],
    author_idx: int,
    hours_ago: int,
    views_count: int,
    *,
    image_index: int | None = None,
    extra_categories: list[str] | None = None,
    video_url: str = '',
) -> dict:
    return {
        'category': category,
        'title': title[:200],
        'lead': lead,
        'paragraphs': paragraphs,
        'tags': tags,
        'author_key': _AUTHOR_KEYS[author_idx % len(_AUTHOR_KEYS)],
        'hours_ago': hours_ago,
        'views_count': views_count,
        **({'image_index': image_index} if image_index is not None else {}),
        **({'extra_categories': extra_categories} if extra_categories else {}),
        **({'video_url': video_url} if video_url else {}),
    }


def _breaking_news() -> list[dict]:
    return [
        _article(
            'breaking_news',
            'Red Sea shipping lane disrupted after coordinated vessel attacks',
            'Major container carriers rerouted dozens of vessels through the Cape of Good Hope on Tuesday after a series of drone and missile strikes targeted commercial traffic in the southern Red Sea, raising freight costs and delivery delays across Europe and Asia.',
            [
                'The U.S. Navy confirmed it intercepted three projectiles near a Liberian-flagged tanker, while Britain\'s maritime authority urged crews to avoid designated high-risk zones. Insurance premiums for transit through the Bab el-Mandeb strait jumped sharply overnight, according to Lloyd\'s Market Association data.',
                'Retailers warned that holiday inventory schedules could slip by two to three weeks if disruptions persist. Analysts at Clarksons Research estimated daily cargo value at risk exceeds $3 billion when including petroleum and consumer goods lanes.',
            ],
            ['Red Sea', 'shipping', 'maritime security', 'global trade'],
            0, 3, 22400,
            image_index=0,
            extra_categories=['world'],
        ),
        _article(
            'breaking_news',
            'Central banks hold emergency call as yen slides to multi-decade low',
            'Finance ministers from Japan, the United States, and South Korea convened an unscheduled video call late Monday after the yen breached 160 per dollar, intensifying speculation that Tokyo may intervene directly in currency markets for the first time this year.',
            [
                'The Bank of Japan reiterated that it would act against excessive volatility, though officials stopped short of confirming imminent dollar sales. Currency traders said option markets were pricing a one-in-three chance of intervention within 48 hours.',
                'Emerging-market currencies with large yen-denominated debt portfolios came under pressure, while export-heavy European automakers saw shares rise on improved competitiveness assumptions.',
            ],
            ['yen', 'forex', 'Bank of Japan', 'intervention'],
            1, 8, 18750,
            image_index=1,
            extra_categories=['economy', 'business'],
        ),
        _article(
            'breaking_news',
            'Wildfire evacuations ordered across Southern California foothills',
            'Authorities expanded mandatory evacuation orders to more than 120,000 residents as hurricane-force Santa Ana winds drove a fast-moving blaze through densely populated suburbs east of Los Angeles, destroying structures and threatening major transmission lines.',
            [
                'Governor Gavin Newsom declared a state of emergency and activated the National Guard to assist with traffic control and shelter operations. Fire officials said containment remained at zero percent due to gusts exceeding 80 mph.',
                'Power utilities preemptively shut electricity to roughly 300,000 customers to reduce ignition risk, complicating evacuation routes and hospital backup systems.',
            ],
            ['wildfire', 'California', 'evacuation', 'climate'],
            2, 5, 25100,
            image_index=2,
            extra_categories=['environment', 'weather'],
        ),
        _article(
            'breaking_news',
            'UN Security Council meets after new satellite images from conflict zone',
            'Diplomats rushed into a closed-door Security Council session after commercial satellite firms published imagery appearing to show large-scale troop movements near a contested border region, reviving fears of a wider regional confrontation.',
            [
                'The Secretary-General urged all parties to restore communication channels and allow humanitarian corridors. Several member states called for an independent verification mission, though veto-wielding powers remained divided on the wording of a draft statement.',
                'Oil futures climbed more than two percent in Asian trading as insurers reassessed war-risk premiums for nearby shipping routes.',
            ],
            ['United Nations', 'Security Council', 'geopolitics', 'conflict'],
            3, 12, 16300,
            image_index=3,
            extra_categories=['world', 'politics'],
        ),
    ]


def _world() -> list[dict]:
    return [
        _article(
            'world',
            'EU leaders agree framework to expand Ukraine reconstruction fund',
            'European Union heads of government endorsed a €50 billion financing envelope aimed at rebuilding energy infrastructure and housing destroyed since 2022, tying disbursements to governance benchmarks and anti-corruption reforms.',
            [
                'Officials in Kyiv welcomed the decision but pressed for faster release of previously pledged military assistance. Hungarian diplomats secured language allowing member states to review annual tranches.',
                'Economists at the European Investment Bank said the package could support up to 400,000 jobs in construction and engineering sectors across Eastern Europe if implementation begins this autumn.',
            ],
            ['European Union', 'Ukraine', 'reconstruction', 'diplomacy'],
            4, 18, 14200,
            image_index=0,
        ),
        _article(
            'world',
            'India surpasses China as world\'s most populous nation, census data shows',
            'Updated demographic projections released by the United Nations Population Division confirm India\'s population at 1.43 billion, while China\'s total declined for a second consecutive year amid rising emigration and lower birth rates.',
            [
                'Policy experts said the milestone will intensify debate over labor-market reform, urban housing, and women\'s workforce participation. Several Indian states are piloting cash incentives for families with two or fewer children.',
                'Manufacturers are expanding southern industrial corridors to capture a youthful labor pool, though skill gaps in advanced manufacturing remain a bottleneck.',
            ],
            ['India', 'demographics', 'population', 'Asia'],
            5, 36, 11800,
            image_index=1,
        ),
        _article(
            'world',
            'Sahel nations form joint counter-terror force after summit in Niamey',
            'Military leaders from Burkina Faso, Mali, and Niger announced a permanent coordination cell to share intelligence and conduct cross-border operations against insurgent groups linked to al-Qaeda and Islamic State affiliates.',
            [
                'Western diplomats expressed concern that the arrangement could complicate United Nations peacekeeping mandates already under strain. Human-rights groups urged independent oversight of detention practices.',
                'France completed the withdrawal of its last permanent base in the region, shifting focus to aerial surveillance partnerships with coastal West African states.',
            ],
            ['Sahel', 'counter-terrorism', 'Africa', 'security'],
            0, 72, 2100,
            image_index=2,
        ),
        _article(
            'world',
            'Antarctic treaty members debate tourism caps amid record visitor season',
            'Delegates at the annual Antarctic Treaty Consultative Meeting proposed binding limits on cruise-ship landings after scientists documented microplastic contamination and disturbance to penguin colonies near popular disembarkation sites.',
            [
                'Tour operators argued that stricter quotas would raise prices and reduce public engagement with climate science. Chile and New Zealand co-sponsored a compromise allowing phased reductions over five seasons.',
                'Researchers presented ice-core data showing accelerated melt on the Antarctic Peninsula, reinforcing calls for tighter environmental protocols.',
            ],
            ['Antarctica', 'tourism', 'climate', 'conservation'],
            1, 120, 890,
            image_index=3,
        ),
    ]


def _politics() -> list[dict]:
    return [
        _article(
            'politics',
            'House passes bipartisan border security bill after months of deadlock',
            'The U.S. House of Representatives approved legislation combining expanded visa verification technology with funding for asylum processing staff, sending the package to the Senate where leaders pledged a vote before the August recess.',
            [
                'Progressive lawmakers criticized provisions requiring local cooperation with federal immigration databases, while conservative members said enforcement measures remained insufficient. The Congressional Budget Office estimated net costs of $4.2 billion over a decade.',
                'White House officials indicated the president would sign the bill if it clears the Senate without major amendments.',
            ],
            ['Congress', 'immigration', 'border security', 'United States'],
            2, 24, 15600,
            image_index=0,
        ),
        _article(
            'politics',
            'UK Labour government unveils first King\'s Speech legislative agenda',
            'Prime Minister Keir Starmer outlined more than 35 bills covering planning reform, renationalization of rail operators, and new workers\' rights, framing the programme as a break from years of political turbulence following Brexit.',
            [
                'The opposition Conservative Party attacked proposed changes to leasehold housing law as unfunded, while business groups welcomed streamlined approval for grid-scale renewable projects.',
                'Constitutional experts noted the speech\'s emphasis on devolving skills funding to regional mayors, signaling a broader decentralization push.',
            ],
            ['United Kingdom', 'Labour', 'King\'s Speech', 'legislation'],
            3, 40, 13400,
            image_index=1,
        ),
        _article(
            'politics',
            'Brazilian Senate opens inquiry into misinformation during municipal elections',
            'A cross-party commission will subpoena social media executives and political consultants after prosecutors presented evidence of coordinated bot networks amplifying false claims about voting machine integrity in October local races.',
            [
                'Platform representatives said they had removed millions of accounts but resisted demands to disclose proprietary ranking algorithms. Free-speech advocates warned against overbroad censorship mandates.',
                'The Supreme Court separately upheld fines against three broadcasters for airing unverified fraud allegations on election night.',
            ],
            ['Brazil', 'misinformation', 'elections', 'social media'],
            4, 96, 1650,
            image_index=2,
        ),
        _article(
            'politics',
            'German coalition negotiates budget after constitutional court ruling',
            'Chancellor Olaf Scholz\'s government scrambled to reallocate €17 billion in spending after a court decision blocked the transfer of pandemic-era funds to climate programmes, forcing cuts to highway maintenance and defence procurement timelines.',
            [
                'The Greens demanded new revenue measures including a wealth surcharge, while the Free Democrats rejected tax increases. Economists warned delayed infrastructure investment could dampen growth next year.',
                'Bundestag leaders scheduled an extraordinary session to pass a revised supplementary budget before the summer break.',
            ],
            ['Germany', 'budget', 'coalition', 'fiscal policy'],
            5, 180, 720,
            image_index=3,
        ),
    ]


def _business() -> list[dict]:
    return [
        _article(
            'business',
            'Apple reports record services revenue as iPhone sales stabilize in China',
            'The technology giant beat Wall Street expectations with quarterly services income of $24.2 billion, offsetting modest hardware declines in Greater China where local competitors gained share with foldable devices.',
            [
                'Chief Executive Tim Cook highlighted growth in payment subscriptions and cloud storage tiers. The company authorized an additional $90 billion share repurchase programme.',
                'Supply-chain executives said diversification into India and Vietnam manufacturing lines reduced concentration risk, though margin pressure from currency swings persisted.',
            ],
            ['Apple', 'earnings', 'technology', 'China'],
            0, 14, 19800,
            image_index=0,
        ),
        _article(
            'business',
            'Boeing reaches tentative labor deal with machinists union',
            'Negotiators for Boeing and the International Association of Machinists agreed on a four-year contract including 38% wage increases and enhanced pension contributions, potentially ending a strike that halted 737 MAX production for six weeks.',
            [
                'Analysts estimated the walkout cost the company more than $5 billion in deferred deliveries. Airlines awaiting MAX jets said they would revise winter schedules if ratification votes fail.',
                'The agreement includes commitments to maintain final assembly in the Seattle region, addressing a central union demand.',
            ],
            ['Boeing', 'labor', 'aviation', 'manufacturing'],
            1, 28, 17200,
            image_index=1,
        ),
        _article(
            'business',
            'Luxury conglomerate LVMH warns of softening demand in mainland China',
            'Shares in LVMH fell after management cited slower growth in Chinese high-end retail, attributing the trend to property-market uncertainty and tighter scrutiny of influencer marketing for premium brands.',
            [
                'Competitors including Hermès and Richemont reported more resilient Asia-Pacific figures, suggesting consumer preferences may be shifting toward smaller leather goods categories.',
                'Analysts trimmed full-year profit forecasts for the sector, though Japanese tourism-linked sales remained robust.',
            ],
            ['LVMH', 'luxury', 'retail', 'China'],
            2, 88, 2400,
            image_index=2,
        ),
        _article(
            'business',
            'Startup funding rebounds in Q2 led by AI infrastructure deals',
            'Venture capital investment in North America rose 18% quarter-on-quarter, driven by mega-rounds for data-center networking firms and enterprise automation platforms, according to PitchBook data released Thursday.',
            [
                'Seed-stage valuations remained disciplined compared with the 2021 peak, while crossover investors returned to pre-IPO rounds for profitable software vendors.',
                'Regulators signaled closer review of acquisitions involving cloud training clusters, citing concentration concerns.',
            ],
            ['venture capital', 'startups', 'AI', 'investment'],
            3, 200, 1100,
            image_index=3,
        ),
    ]


def _economy() -> list[dict]:
    return [
        _article(
            'economy',
            'Federal Reserve signals patience as inflation metrics show uneven progress',
            'Chair Jerome Powell said policymakers need greater confidence that price pressures are sustainably easing before cutting interest rates, noting resilient services inflation and rising shelter costs in the latest consumer price index report.',
            [
                'Futures markets pushed back the first expected rate reduction to December from September. Treasury yields climbed across the curve, lifting mortgage rates above 7% again.',
                'Regional Fed presidents diverged publicly, with some advocating preemptive cuts to protect labor markets and others warning against easing too soon.',
            ],
            ['Federal Reserve', 'inflation', 'interest rates', 'monetary policy'],
            4, 22, 12100,
            image_index=0,
        ),
        _article(
            'economy',
            'Eurozone unemployment falls to record low despite manufacturing slump',
            'Eurostat reported a jobless rate of 6.4%, even as factory output contracted for an eighth month in Germany and Italy, highlighting a split between services hiring and industrial weakness.',
            [
                'Economists said tight labor markets could keep wage growth elevated, complicating the European Central Bank\'s effort to bring inflation back to its 2% target.',
                'Youth unemployment improved in Spain and Greece following tourism-season hiring, though long-term vacancy rates in tech skills remain elevated.',
            ],
            ['Eurozone', 'employment', 'manufacturing', 'ECB'],
            5, 64, 1950,
            image_index=1,
        ),
        _article(
            'economy',
            'IMF upgrades global growth forecast on resilient U.S. consumer spending',
            'The International Monetary Fund raised its 2025 world GDP projection to 3.2%, citing stronger-than-expected retail sales and fiscal stimulus in major economies, while warning that geopolitical shocks could quickly reverse gains.',
            [
                'Emerging markets benefited from stable commodity prices, though several low-income nations face refinancing cliffs as commercial debt matures.',
                'The report urged coordinated investment in green infrastructure to avoid a prolonged productivity slowdown.',
            ],
            ['IMF', 'global growth', 'GDP', 'forecast'],
            0, 140, 780,
            image_index=2,
        ),
        _article(
            'economy',
            'Argentina secures new IMF review after peso stabilisation measures',
            'The Fund\'s executive board confirmed disbursement of a $4.7 billion tranche following Buenos Aires\' progress on fiscal consolidation and central bank reserve accumulation under President Javier Milei\'s austerity programme.',
            [
                'Street protests erupted over cuts to university subsidies, but bond spreads narrowed as investors welcomed primary surplus targets.',
                'Analysts cautioned that drought-sensitive agricultural exports remain a key swing factor for currency stability.',
            ],
            ['Argentina', 'IMF', 'peso', 'Latin America'],
            1, 260, 540,
            image_index=3,
        ),
    ]


def _technology() -> list[dict]:
    return [
        _article(
            'technology',
            'OpenAI unveils next-generation model with improved reasoning benchmarks',
            'The artificial intelligence lab released a flagship system demonstrating significant gains on graduate-level science and coding evaluations, while adding configurable safety layers for enterprise customers in regulated industries.',
            [
                'Chief technology officers at Fortune 500 firms said pilot programmes would expand to financial compliance and drug-discovery workflows. Competitors accelerated roadmap announcements from Google DeepMind and Anthropic.',
                'Regulators in the European Union requested documentation on training data provenance ahead of enforcement of the AI Act\'s high-risk system requirements.',
            ],
            ['OpenAI', 'artificial intelligence', 'machine learning', 'enterprise'],
            2, 6, 24300,
            image_index=0,
        ),
        _article(
            'technology',
            'EU opens antitrust probe into cloud licensing practices',
            'European Commission investigators sent questionnaires to major software vendors examining whether bundling rules unfairly penalize customers who migrate workloads to rival hyperscale providers.',
            [
                'Microsoft said it would cooperate fully and pointed to recent licensing reforms. Amazon and Google Cloud welcomed the inquiry, arguing restrictive terms inflate switching costs for public-sector agencies.',
                'Industry groups warned lengthy proceedings could delay digital transformation projects across member states.',
            ],
            ['antitrust', 'cloud computing', 'European Union', 'Microsoft'],
            3, 48, 3200,
            image_index=1,
        ),
        _article(
            'technology',
            'TSMC begins mass production at Arizona fab amid talent recruitment drive',
            'Taiwan Semiconductor Manufacturing Company confirmed initial output of 4-nanometre chips at its Phoenix facility, supported by federal grants and partnerships with local universities to train technicians.',
            [
                'Customers including Apple and Nvidia said U.S.-based production would diversify supply chains exposed to Taiwan Strait tensions. Construction on a second Arizona fab remains on schedule for 2028.',
                'Labour advocates raised concerns about shift schedules and subcontractor safety standards at the site.',
            ],
            ['TSMC', 'semiconductors', 'manufacturing', 'Arizona'],
            4, 110, 1750,
            image_index=2,
        ),
        _article(
            'technology',
            'Cybersecurity firms warn of supply-chain attack targeting npm packages',
            'Researchers identified malicious updates to widely downloaded JavaScript libraries that exfiltrated developer credentials, prompting GitHub and npm maintainers to revoke compromised tokens and publish hardened verification tools.',
            [
                'Corporate security teams scanned internal repositories overnight, while insurance underwriters reassessed coverage terms for open-source dependency risks.',
                'Governments encouraged adoption of software bill-of-materials standards for critical infrastructure vendors.',
            ],
            ['cybersecurity', 'npm', 'supply chain', 'software'],
            5, 320, 620,
            image_index=3,
        ),
    ]


def _science() -> list[dict]:
    return [
        _article(
            'science',
            'James Webb telescope detects water vapor in exoplanet atmosphere',
            'Astronomers using the space observatory confirmed spectroscopic signatures of water vapor and carbon dioxide in the atmosphere of a temperate Neptune-sized planet orbiting a star 120 light-years from Earth.',
            [
                'The findings, published in Nature, suggest rocky-core planets may retain atmospheres long enough for liquid water under certain conditions. Follow-up observations with ground-based interferometers are scheduled.',
                'NASA officials said the result validates Webb\'s mid-infrared instrument performance after a year of calibration refinements.',
            ],
            ['James Webb', 'exoplanet', 'astronomy', 'NASA'],
            0, 52, 2800,
            image_index=0,
        ),
        _article(
            'science',
            'CRISPR trial shows durable reduction in cholesterol for genetic disorder',
            'Clinical researchers reported that a single infusion of base-editing therapy lowered LDL cholesterol by more than 50% for at least 18 months in patients with familial hypercholesterolemia, a milestone for in vivo gene editing.',
            [
                'Independent monitors recorded no serious adverse events related to the treatment. Regulators in the United States and United Kingdom opened accelerated review pathways.',
                'Ethicists urged transparent consent processes given irreversible genomic changes and long follow-up requirements.',
            ],
            ['CRISPR', 'gene editing', 'medicine', 'clinical trial'],
            1, 130, 1540,
            image_index=1,
        ),
        _article(
            'science',
            'Quantum computer achieves error correction threshold in new experiment',
            'Google Quantum AI demonstrated logical qubits with error rates below the threshold required for scalable computation, using a surface-code architecture with improved two-qubit gate fidelity.',
            [
                'Physicists cautioned that practical advantage for chemistry simulations remains years away, but investors sent quantum computing stocks higher on the announcement.',
                'National laboratories expanded partnerships to test hybrid classical-quantum workflows for materials discovery.',
            ],
            ['quantum computing', 'Google', 'physics', 'research'],
            2, 210, 980,
            image_index=2,
        ),
        _article(
            'science',
            'Deep-sea expedition maps hydrothermal vents teeming with unknown species',
            'An international research vessel returned from the South Pacific with more than 30 candidate new species collected near volcanic vents, including blind shrimp and bacteria capable of metabolizing hydrogen sulfide at extreme temperatures.',
            [
                'Marine biologists said the discoveries could inform extremophile research relevant to astrobiology. Mining regulators debated whether to expand protected zones before seabed extraction permits are issued.',
                'All specimens will be catalogued under an open-access genomic repository hosted by the Smithsonian Institution.',
            ],
            ['marine biology', 'deep sea', 'biodiversity', 'expedition'],
            3, 400, 410,
            image_index=3,
        ),
    ]


def _health() -> list[dict]:
    return [
        _article(
            'health',
            'WHO declares mpox no longer a global health emergency',
            'The World Health Organization lifted its highest alert level for mpox after sustained declines in case counts across Central Africa and improved vaccine access, while urging countries to maintain surveillance for new clade variants.',
            [
                'Public health officials credited community engagement and targeted ring vaccination in outbreak hotspots. Donor agencies committed continued funding for laboratory capacity in underserved regions.',
                'Clinicians emphasized that immunocompromised patients still face elevated severity risks requiring rapid antiviral access.',
            ],
            ['WHO', 'mpox', 'public health', 'vaccines'],
            4, 30, 10900,
            image_index=0,
        ),
        _article(
            'health',
            'Ozempic supply constraints ease as Novo Nordisk expands production',
            'The Danish pharmaceutical company said new manufacturing lines in Denmark and the United States would increase GLP-1 agonist output by 40% next year, addressing shortages that frustrated diabetes and obesity patients worldwide.',
            [
                'Insurers tightened prior-authorization rules amid debate over long-term cost-effectiveness. Compounding pharmacies face tighter FDA scrutiny over unapproved formulations.',
                'Cardiologists reported emerging data suggesting benefits beyond weight loss, including reductions in major adverse cardiovascular events.',
            ],
            ['Ozempic', 'GLP-1', 'pharmaceuticals', 'obesity'],
            5, 84, 2300,
            image_index=1,
        ),
        _article(
            'health',
            'Study links ultra-processed food intake to faster cognitive decline',
            'A longitudinal cohort study tracking 14,000 adults over a decade found that diets high in ultra-processed products correlated with accelerated memory loss, independent of calorie intake and exercise levels.',
            [
                'Nutrition scientists called for clearer front-of-pack labeling policies, while food industry groups questioned causality and highlighted reformulation efforts reducing sodium and sugar.',
                'Policy makers in Chile and Mexico cited the findings in renewed debates over advertising restrictions targeting children.',
            ],
            ['nutrition', 'dementia', 'public health', 'research'],
            0, 160, 1320,
            image_index=2,
        ),
        _article(
            'health',
            'NHS pilots AI triage tool in emergency departments across England',
            'Hospitals in Manchester and Birmingham began testing an algorithm that prioritizes patients based on vital signs and symptom narratives, aiming to reduce average wait times during winter surge periods.',
            [
                'Clinician unions demanded human oversight for all disposition decisions and transparency on training datasets. Privacy advocates raised questions about retention of sensitive consultation transcripts.',
                'Early results showed modest improvements in time-to-treatment for high-acuity cases without increasing mortality indicators.',
            ],
            ['NHS', 'artificial intelligence', 'emergency care', 'triage'],
            1, 280, 670,
            image_index=3,
        ),
    ]


def _sports() -> list[dict]:
    return [
        _article(
            'sports',
            'Real Madrid clinches Champions League title in penalty shootout thriller',
            'Real Madrid captured a record-extending 16th European crown after a 1-1 draw against Manchester City culminated in a dramatic shootout, with goalkeeper Thibaut Courtois saving two penalties in Istanbul.',
            [
                'Manager Carlo Ancelotti praised squad depth following injuries to key midfielders mid-season. UEFA announced record broadcast revenue distribution exceeding €2.5 billion to participating clubs.',
                'Fan zones across Madrid erupted in celebration, while authorities reported largely peaceful crowds with minor post-match disturbances near the city centre.',
            ],
            ['Champions League', 'Real Madrid', 'football', 'UEFA'],
            2, 4, 26800,
            image_index=0,
        ),
        _article(
            'sports',
            'Simone Biles returns to win all-around gold at world gymnastics championships',
            'American superstar Simone Biles posted the highest all-around score of the quadrennial cycle, landing a Yurchenko double pike vault that will bear her name in the sport\'s official code of points.',
            [
                'Teammates secured team silver behind Brazil\'s historic first world team title. International Gymnastics Federation officials said scoring reforms introduced this season rewarded difficulty more transparently.',
                'Biles hinted she would evaluate her schedule month-by-month ahead of the Paris Olympic cycle\'s final major events.',
            ],
            ['gymnastics', 'Simone Biles', 'world championships', 'Olympics'],
            3, 16, 18900,
            image_index=1,
        ),
        _article(
            'sports',
            'NBA approves expanded replay review for foul decisions in final two minutes',
            'Team governors voted to grant the league office authority to overturn certain personal foul calls using centralized replay officials, a change prompted by high-profile postseason controversies.',
            [
                'The players\' association supported the move but requested consultation on workload impacts for referees. Coaches debated whether pace of play would suffer from additional stoppages.',
                'Implementation begins at the start of the upcoming regular season with training camps for officiating crews.',
            ],
            ['NBA', 'basketball', 'replay review', 'officiating'],
            4, 76, 2100,
            image_index=2,
        ),
        _article(
            'sports',
            'Cricket\'s T20 World Cup expands to 24 teams with new Americas qualifier',
            'The International Cricket Council confirmed format changes adding four berths and introducing regional qualifiers designed to grow participation in the United States ahead of co-hosted tournaments.',
            [
                'Broadcasters secured multi-year rights deals emphasizing short-form highlights for mobile audiences. Purists argued dilution of quality could reduce competitive balance in the group stage.',
                'USA Cricket Federation unveiled high-performance centres in Texas and New Jersey supported by franchise league investors.',
            ],
            ['cricket', 'T20', 'World Cup', 'ICC'],
            5, 190, 890,
            image_index=3,
        ),
    ]


def _entertainment() -> list[dict]:
    return [
        _article(
            'entertainment',
            'Streaming wars pivot as Netflix raises prices and cracks down on password sharing',
            'Netflix told investors that paid sharing and an ad-supported tier pushed subscriber growth above forecasts, announcing modest price increases in the United States and Britain effective next month.',
            [
                'Rivals Disney+ and Max responded with bundled promotional offers ahead of the holiday release calendar. Analysts said churn remained manageable despite competitive content spending.',
                'Hollywood unions monitored residual payments closely as studios greenlit fewer mid-budget theatrical releases.',
            ],
            ['Netflix', 'streaming', 'television', 'media'],
            0, 20, 14700,
            image_index=0,
        ),
        _article(
            'entertainment',
            'Venice Film Festival opens with standing ovation for refugee drama',
            'The premiere of "Silent Harbour," chronicling a family\'s Mediterranean crossing, received an eight-minute ovation and early Oscar buzz for its lead performances and cinematography.',
            [
                'Festival director Alberto Barbera said the lineup balanced auteur cinema with genre titles aimed at younger audiences. Sales agents reported strong interest from North American distributors.',
                'Protests outside the venue called for greater industry support for migrant storytellers beyond festival spotlight moments.',
            ],
            ['Venice Film Festival', 'cinema', 'Oscars', 'film'],
            1, 44, 12800,
            image_index=1,
        ),
        _article(
            'entertainment',
            'Taylor Swift Eras Tour film crosses $400 million in global box office',
            'The concert film continued defying theatrical slowdown trends, prompting exhibitors to add sing-along screenings and extend runs through January.',
            [
                'Music industry analysts said the release redefined event cinema for touring artists, influencing planning for upcoming stadium tours.',
                'Swift\'s re-recorded catalogue simultaneously dominated streaming charts, illustrating cross-platform audience engagement.',
            ],
            ['Taylor Swift', 'music', 'box office', 'concert film'],
            2, 100, 2400,
            image_index=2,
        ),
        _article(
            'entertainment',
            'Video game actors union reaches deal on AI performance protections',
            'SAG-AFTRA and major publishers agreed to consent requirements and compensation when digital replicas of voice and motion-capture performances are used in future titles.',
            [
                'Developers said guardrails provide clarity for prototyping tools while preserving creative flexibility. Indie studios requested phased compliance timelines.',
                'The agreement follows a 2024 strike that delayed several AAA releases.',
            ],
            ['video games', 'SAG-AFTRA', 'AI', 'labor'],
            3, 240, 1100,
            image_index=3,
        ),
    ]


def _culture() -> list[dict]:
    return [
        _article(
            'culture',
            'Louvre reopens wing after four-year renovation of Egyptian antiquities',
            'Parisians queued before dawn as the museum unveiled redesigned galleries featuring improved climate control and augmented-reality guides explaining provenance research on contested artefacts.',
            [
                'Culture Minister Rachida Dati said the project exemplified France\'s commitment to accessible heritage. Repatriation advocates maintained pressure for return of items acquired during colonial expeditions.',
                'Ticket demand prompted timed-entry extensions through the autumn tourist season.',
            ],
            ['Louvre', 'museum', 'heritage', 'Paris'],
            4, 60, 1800,
            image_index=0,
        ),
        _article(
            'culture',
            'Nobel Prize in Literature awarded to poet chronicling diaspora identity',
            'The Swedish Academy honoured Kenyan-born writer Amara Njeri for verse that "maps memory across continents with unsentimental precision," sparking celebratory readings from Nairobi to London.',
            [
                'Booksellers reported overnight sell-outs of Njeri\'s out-of-print collections. Critics debated whether the choice signals renewed attention to poetry amid dominance of narrative nonfiction.',
                'Njeri pledged to fund rural library programmes with a portion of the prize stipend.',
            ],
            ['Nobel Prize', 'literature', 'poetry', 'awards'],
            5, 150, 920,
            image_index=1,
        ),
        _article(
            'culture',
            'Broadway season sets attendance record on diverse casting and new musicals',
            'The Broadway League reported grosses exceeding $1.9 billion as productions featuring majority-minority creative teams drew younger audiences and strong tourist conversions.',
            [
                'Producers credited dynamic pricing models and social media marketing partnerships. Union stagehands secured wage increases in renewed contracts.',
                'Several plays addressing artificial intelligence ethics became surprise critical hits.',
            ],
            ['Broadway', 'theatre', 'New York', 'performing arts'],
            0, 220, 740,
            image_index=2,
        ),
        _article(
            'culture',
            'UNESCO adds traditional tea ceremonies to intangible heritage list',
            'Delegations from China, Japan, and Morocco celebrated the inscription of distinct tea rituals, emphasizing intergenerational transmission and community gathering functions.',
            [
                'Commercial tea brands pledged marketing campaigns highlighting artisan growers. Anthropologists noted growing interest among urban youth reviving ceremonial practices.',
                'Tourism boards developed cultural routes linking heritage sites with tasting workshops.',
            ],
            ['UNESCO', 'heritage', 'tea', 'tradition'],
            1, 360, 380,
            image_index=3,
        ),
    ]


def _lifestyle() -> list[dict]:
    return [
        _article(
            'lifestyle',
            'Digital detox retreats surge in popularity among burned-out professionals',
            'Wellness operators from Costa Rica to the Scottish Highlands report wait lists for phone-free programmes combining forest bathing, guided journaling, and sleep hygiene coaching.',
            [
                'Psychologists say structured disconnection can reduce cortisol markers over week-long stays, though benefits fade without ongoing boundary-setting at work.',
                'Corporate HR departments began subsidizing partial tuition as part of mental-health benefits packages.',
            ],
            ['wellness', 'digital detox', 'mental health', 'travel'],
            2, 80, 1600,
            image_index=0,
        ),
        _article(
            'lifestyle',
            'Minimalist wardrobe trends reshape fast-fashion demand among Gen Z',
            'Retail analysts document growing resale and rental adoption as young consumers prioritize capsule wardrobes and durability certifications over seasonal micro-trends.',
            [
                'Platforms like Depop and Vinted expanded authentication services for luxury items. Mainstream brands launched repair programmes to retain customers.',
                'Environmental groups cautioned that overproduction continues despite shifting attitudes in urban markets.',
            ],
            ['fashion', 'sustainability', 'Gen Z', 'retail'],
            3, 170, 880,
            image_index=1,
        ),
        _article(
            'lifestyle',
            'Remote work hybrid policies stabilize as companies mandate two office days',
            'A survey of 500 multinational employers found most settled on two to three in-office days weekly, balancing collaboration needs with employee retention concerns.',
            [
                'Commercial real estate owners adapted suburban hubs near commuter rail lines. Employees cited reduced commute stress but noted ergonomic challenges in home setups.',
                'Labour lawyers reported increased litigation over reimbursement for home office equipment.',
            ],
            ['remote work', 'hybrid', 'workplace', 'productivity'],
            4, 300, 520,
            image_index=2,
        ),
        _article(
            'lifestyle',
            'Plant-based dining goes mainstream as Michelin stars multiply for vegan kitchens',
            'Fine-dining guides awarded stars to twelve fully plant-based restaurants globally this year, reflecting chef innovation with fermented proteins and regional produce.',
            [
                'Food critics said tasting menus now rival traditional establishments in complexity and price. Grocery chains expanded chilled vegan ranges in response.',
                'Nutritionists encouraged diners to monitor sodium levels in highly processed meat alternatives.',
            ],
            ['vegan', 'food', 'Michelin', 'dining'],
            5, 480, 290,
            image_index=3,
        ),
    ]


def _opinion() -> list[dict]:
    return [
        _article(
            'opinion',
            'The case for taxing carbon at the border, not just the smokestack',
            'Border-adjustment mechanisms can align domestic manufacturers with climate goals while preventing leakage to jurisdictions with weaker standards — if designed with developing-country exemptions.',
            [
                'Critics argue administrative complexity will invite litigation and retaliation. Evidence from early EU CBAM pilots suggests transparency alone shifts supplier behaviour.',
                'Policymakers should pair tariffs with technology-transfer funds to avoid punitive optics.',
            ],
            ['carbon tax', 'climate policy', 'trade', 'editorial'],
            0, 90, 1400,
            image_index=0,
        ),
        _article(
            'opinion',
            'AI literacy must become a core curriculum requirement, not an elective',
            'Students entering a workforce transformed by generative tools need critical evaluation skills, not just prompt-engineering tricks taught in after-school clubs.',
            [
                'Teachers require professional development funding and guardrails against vendor-driven curricula. Libraries can serve as neutral hubs for public education.',
                'Democratic resilience depends on populations that understand both capabilities and failure modes of automated systems.',
            ],
            ['education', 'AI literacy', 'schools', 'editorial'],
            1, 200, 650,
            image_index=1,
        ),
        _article(
            'opinion',
            'Housing affordability demands zoning courage, not another study commission',
            'Incremental upzoning near transit nodes consistently increases supply faster than subsidy-only approaches, yet local councils continue deferring votes to appease incumbent homeowners.',
            [
                'Renters organizing in Auckland and Minneapolis show coalitions can counter NIMBY pressure when data on displacement is presented transparently.',
                'Federal governments should tie infrastructure grants to measurable permit reform outcomes.',
            ],
            ['housing', 'zoning', 'affordability', 'editorial'],
            2, 340, 480,
            image_index=2,
        ),
        _article(
            'opinion',
            'Why independent journalism needs antitrust scrutiny of ad tech giants',
            'Concentrated programmatic advertising markets siphon revenue from publishers while incentivizing engagement-bait content — undermining the information ecosystem democracies require.',
            [
                'Breakups alone won\'t suffice without privacy-preserving alternatives that restore bargaining power to newsrooms.',
                'Public-interest media funds should complement structural remedies, not replace them.',
            ],
            ['journalism', 'antitrust', 'media', 'editorial'],
            3, 520, 320,
            image_index=3,
        ),
    ]


def _education() -> list[dict]:
    return [
        _article(
            'education',
            'Finland pilots AI tutors in mathematics while keeping teachers in the loop',
            'Selected secondary schools began deploying adaptive learning platforms that generate practice problems and immediate feedback, with educators reviewing analytics dashboards to intervene when students plateau.',
            [
                'Union leaders conditioned support on guarantees that AI tools supplement rather than replace instructional hours. Researchers will publish outcomes after two academic terms.',
                'Parents welcomed transparency reports detailing data retention policies for minors.',
            ],
            ['Finland', 'AI tutors', 'mathematics', 'schools'],
            4, 70, 1700,
            image_index=0,
        ),
        _article(
            'education',
            'U.S. student loan forgiveness programme faces Supreme Court review',
            'Justices agreed to hear challenges to executive action cancelling debt for public-sector workers meeting decade-long payment thresholds, with implications for millions of borrowers.',
            [
                'Legal scholars differ on whether the Education Department exceeded statutory authority. Borrowers awaiting relief described financial planning paralysis.',
                'Congressional leaders proposed legislative codification regardless of the court\'s eventual ruling.',
            ],
            ['student loans', 'Supreme Court', 'United States', 'higher education'],
            5, 160, 980,
            image_index=1,
        ),
        _article(
            'education',
            'Global literacy rates stall as pandemic learning loss persists in low-income regions',
            'UNESCO\'s annual report found 763 million adults still lack basic literacy skills, with girls in sub-Saharan Africa disproportionately affected by school closures and teacher shortages.',
            [
                'Donors pledged $1.2 billion for accelerated catch-up programmes emphasizing phonics and mother-tongue instruction.',
                'Technology-heavy solutions faced criticism where electricity and device access remain unreliable.',
            ],
            ['UNESCO', 'literacy', 'education', 'development'],
            0, 250, 590,
            image_index=2,
        ),
        _article(
            'education',
            'Oxford and Cambridge report record international applicant numbers post-Brexit visa reforms',
            'Russell Group universities said streamlined graduate visa routes boosted applications from India and Nigeria, though housing shortages in college towns intensified.',
            [
                'Domestic students raised concerns about competition for limited tutorial slots. Institutions expanded foundation-year pathways for underrepresented UK regions.',
                'Tuition-dependent budgets remain exposed to currency fluctuations affecting overseas fee payers.',
            ],
            ['Oxford', 'Cambridge', 'universities', 'Brexit'],
            1, 440, 350,
            image_index=3,
        ),
    ]


def _environment() -> list[dict]:
    return [
        _article(
            'environment',
            'COP29 delegates agree to triple climate finance for adaptation by 2030',
            'Negotiators in Baku finalized a framework requiring developed nations to mobilize $300 billion annually for adaptation grants, though critics said the figure falls short of vulnerable countries\' stated needs.',
            [
                'Island states secured language referencing loss-and-damage funding mechanisms. Fossil-fuel lobbyists faced stricter accreditation rules after prior controversies.',
                'Markets reacted modestly as the agreement lacked binding national emission-reduction schedules.',
            ],
            ['COP29', 'climate finance', 'adaptation', 'UN'],
            2, 38, 11500,
            image_index=0,
        ),
        _article(
            'environment',
            'Amazon deforestation rate drops to 15-year low after enforcement surge',
            'Brazilian environmental agencies reported a 40% decline in cleared rainforest area, attributing gains to satellite monitoring and increased fines against illegal cattle ranching.',
            [
                'Indigenous leaders cautioned that proposed highway projects could reverse progress. Commodity traders expanded traceability requirements for soy and beef exports.',
                'Scientists warned that drought conditions may increase fire risk during the upcoming dry season.',
            ],
            ['Amazon', 'deforestation', 'Brazil', 'conservation'],
            3, 110, 2100,
            image_index=1,
        ),
        _article(
            'environment',
            'North Atlantic current weakening faster than models projected, study finds',
            'Oceanographers publishing in Science documented a 15% slowdown in Atlantic Meridional Overturning Circulation over four decades, raising concerns about European weather pattern shifts.',
            [
                'Climate models differ on tipping-point timelines, but authors urged aggressive emission cuts to reduce tail risks.',
                'Fishing communities reported changing migration routes for cod and mackerel stocks.',
            ],
            ['ocean currents', 'climate change', 'Atlantic', 'research'],
            4, 230, 820,
            image_index=2,
        ),
        _article(
            'environment',
            'Solar capacity additions set record as battery storage costs plummet',
            'The International Energy Agency said renewables accounted for 90% of new power capacity globally last year, driven by utility-scale solar paired with four-hour lithium-ion storage systems.',
            [
                'Grid operators upgraded interconnection queues to address backlog delays in the United States.',
                'Recycling firms scaled processes for end-of-life panels amid forecasts of a retirement wave after 2035.',
            ],
            ['solar energy', 'renewables', 'battery storage', 'IEA'],
            5, 380, 440,
            image_index=3,
        ),
    ]


def _crime() -> list[dict]:
    return [
        _article(
            'crime',
            'International task force dismantles cryptocurrency laundering network',
            'Law enforcement agencies across Europe and Asia arrested 42 suspects accused of moving more than $600 million through nested exchanges and privacy coins to obscure ransomware proceeds.',
            [
                'Prosecutors said the operation relied on undercover agents infiltrating encrypted messaging channels. Exchanges cooperated by freezing wallets linked to sanctioned entities.',
                'Cybersecurity firms urged victims to report incidents quickly to improve recovery rates.',
            ],
            ['cryptocurrency', 'money laundering', 'cybercrime', 'police'],
            0, 55, 1900,
            image_index=0,
        ),
        _article(
            'crime',
            'Major art theft ring convicted over museum burglaries spanning decade',
            'A Dutch court sentenced five defendants to prison terms for stealing masterpieces valued at €100 million, later recovered from a Romania warehouse after an informant tip.',
            [
                'Museums accelerated adoption of smart sensors and provenance databases. Insurers raised premiums for institutions with outdated alarm systems.',
                'Investigators praised cross-border coordination through Europol\'s art crime unit.',
            ],
            ['art theft', 'court', 'Europol', 'museums'],
            1, 145, 1100,
            image_index=1,
        ),
        _article(
            'crime',
            'Fentanyl precursor crackdown leads to record seizures at Pacific ports',
            'U.S. Customs and Border Protection reported interdicting 12 tonnes of precursor chemicals this fiscal year, coordinating with Mexican authorities on upstream manufacturing raids.',
            [
                'Public health officials said street potency variations continue driving overdose deaths despite supply disruptions.',
                'Diplomats discussed expanded chemical-tracking treaties at a regional summit.',
            ],
            ['fentanyl', 'drug enforcement', 'border', 'public safety'],
            2, 270, 680,
            image_index=2,
        ),
        _article(
            'crime',
            'Corporate whistleblower awarded $24 million in securities fraud case',
            'The U.S. Securities and Exchange Commission paid a record bounty to a former finance executive whose tips exposed accounting fraud at a publicly traded healthcare conglomerate.',
            [
                'Legal experts said the award may encourage reporting despite non-disclosure agreements. The company agreed to a deferred prosecution arrangement with compliance monitorship.',
                'Shareholders filed parallel class-action suits seeking damages.',
            ],
            ['SEC', 'whistleblower', 'securities fraud', 'corporate crime'],
            3, 500, 360,
            image_index=3,
        ),
    ]


def _travel() -> list[dict]:
    return [
        _article(
            'travel',
            'Japan lifts daily arrival cap as yen weakness fuels tourism boom',
            'Inbound visitors exceeded pre-pandemic records, with Kyoto and Hokkaido reporting hotel occupancy above 90% during cherry blossom and ski seasons.',
            [
                'Authorities deployed multilingual crowd-control staff at popular shrines. Locals debated balancing hospitality revenue with neighbourhood congestion.',
                'Rail operators added luggage-forwarding services for international passengers.',
            ],
            ['Japan', 'tourism', 'yen', 'travel'],
            4, 65, 2200,
            image_index=0,
        ),
        _article(
            'travel',
            'EU digital border system EES launch delayed again to late 2025',
            'Member states cited incomplete biometric kiosk installations at land crossings, postponing mandatory fingerprint checks for non-EU travellers entering the Schengen area.',
            [
                'Airlines warned of potential check-in delays once enforcement begins. Privacy regulators reviewed data retention limits for entry-exit records.',
                'Tour operators adjusted summer packaging timelines accordingly.',
            ],
            ['European Union', 'border control', 'EES', 'Schengen'],
            5, 180, 950,
            image_index=1,
        ),
        _article(
            'travel',
            'Sustainable aviation fuel mandates take effect on select transatlantic routes',
            'Carriers operating between Europe and North America must blend at least 2% SAF on departures from major hubs, with penalties for non-compliance beginning January.',
            [
                'Producers raced to scale waste-oil conversion plants despite feedstock competition from road biodiesel.',
                'Passengers face modest fare surcharges earmarked for SAF procurement funds.',
            ],
            ['aviation', 'SAF', 'sustainability', 'regulation'],
            0, 310, 580,
            image_index=2,
        ),
        _article(
            'travel',
            'Patagonia trekking permits sell out in minutes amid influencer-driven demand',
            'Chile\'s national park service introduced lottery allocations for the W Trek after viral social media posts overwhelmed reservation systems and raised safety concerns on narrow trails.',
            [
                'Guiding companies hired additional wilderness medics. Environmentalists urged visitors to respect leave-no-trace protocols in fragile ecosystems.',
                'Alternative routes in less trafficked regions saw increased promotion.',
            ],
            ['Patagonia', 'hiking', 'tourism', 'Chile'],
            1, 550, 310,
            image_index=3,
        ),
    ]


def _food() -> list[dict]:
    return [
        _article(
            'food',
            'Olive oil prices retreat from record highs as Mediterranean harvest improves',
            'Spanish and Italian producers forecast yields up 20% year-on-year after favourable spring rains, easing pantry-staple inflation that squeezed households throughout 2024.',
            [
                'Retailers reduced shelf prices gradually, citing long-term supplier contracts. Fraud inspectors increased testing for adulterated blends.',
                'Restaurateurs reintroduced olive-oil-forward dishes previously removed from menus.',
            ],
            ['olive oil', 'food prices', 'Mediterranean', 'agriculture'],
            2, 95, 1500,
            image_index=0,
        ),
        _article(
            'food',
            'FDA approves lab-grown chicken for nationwide restaurant sales',
            'Upside Foods received clearance to supply cultivated poultry to a chain of fast-casual outlets, marking the first broad U.S. commercial deployment of cell-based meat.',
            [
                'Consumer acceptance surveys show curiosity among urban diners but scepticism in rural markets. Animal-welfare groups welcomed reduced slaughter volumes.',
                'Producers must label products clearly and submit to facility inspections.',
            ],
            ['lab-grown meat', 'FDA', 'food tech', 'restaurants'],
            3, 210, 870,
            image_index=1,
        ),
        _article(
            'food',
            'Coffee leaf rust resurgence threatens Central American smallholder farms',
            'Agricultural extension services reported outbreaks across Guatemala and Honduras, prompting emergency fungicide subsidies and shade-tree planting programmes.',
            [
                'Climate variability extends spore viability at higher altitudes previously considered safe. Fair-trade cooperatives sought buyer commitments to absorb short-term yield declines.',
                'Roasters diversified sourcing to East African arabica beans.',
            ],
            ['coffee', 'agriculture', 'Central America', 'climate'],
            4, 350, 490,
            image_index=2,
        ),
        _article(
            'food',
            'Michelin Guide expands street food category across Southeast Asia',
            'Bangkok and Kuala Lumpur vendors received inaugural Bib Gourmand distinctions for hawker stalls serving boat noodles, satay, and regional curries at accessible price points.',
            [
                'Tourism boards launched maps highlighting recognised stalls. Critics asked whether acclaim would price out local regulars.',
                'Hygiene inspectors collaborated on training rather than punitive closures.',
            ],
            ['street food', 'Michelin', 'Southeast Asia', 'dining'],
            5, 600, 280,
            image_index=3,
        ),
    ]


def _real_estate() -> list[dict]:
    return [
        _article(
            'real_estate',
            'U.S. existing home sales hit 30-year low as mortgage rates bite',
            'The National Association of Realtors reported annualized sales below four million units, with homeowners reluctant to relinquish low fixed-rate mortgages obtained during the pandemic era.',
            [
                'Builders focused on smaller-footprint starter homes with rate-buydown incentives. Rental demand kept vacancy rates tight in Sun Belt metros.',
                'Economists expect turnover to recover only gradually unless rates decline materially.',
            ],
            ['housing market', 'mortgages', 'real estate', 'United States'],
            0, 75, 1800,
            image_index=0,
        ),
        _article(
            'real_estate',
            'Dubai luxury property transactions surge on golden visa incentives',
            'High-net-worth buyers from Russia, India, and Britain drove record off-plan sales on Palm Jumeirah and Downtown districts, despite global interest-rate headwinds.',
            [
                'Developers offered cryptocurrency payment options at select launches. Analysts warned of oversupply risk in the mid-market segment.',
                'Regulators tightened anti-money-laundering checks on beneficial ownership structures.',
            ],
            ['Dubai', 'luxury property', 'real estate', 'investment'],
            1, 190, 920,
            image_index=1,
        ),
        _article(
            'real_estate',
            'Commercial office vacancy rates plateau in major European capitals',
            'CBRE data show London and Frankfurt vacancies stabilizing near 10% as landlords convert underperforming towers to residential and life-sciences labs.',
            [
                'Hybrid work policies remain entrenched, limiting full recovery to pre-2020 occupancy.',
                'Green retrofit grants accelerated adoption of heat-pump and facade upgrades.',
            ],
            ['commercial real estate', 'office vacancy', 'Europe', 'CBRE'],
            2, 330, 560,
            image_index=2,
        ),
        _article(
            'real_estate',
            'Canada introduces two-year cap on international student housing permits in hotspots',
            'Municipalities with rental vacancy below 2% may restrict new purpose-built student accommodations linked to visa enrolments, aiming to ease pressure on local tenants.',
            [
                'Universities argued caps could reduce revenue for campus expansions. Tenant advocates called for complementary social-housing investments.',
                'Provincial governments retain override authority in designated growth corridors.',
            ],
            ['Canada', 'housing', 'students', 'policy'],
            3, 580, 340,
            image_index=3,
        ),
    ]


def _weather() -> list[dict]:
    return [
        _article(
            'weather',
            'Atlantic hurricane season forecast upgraded to above-normal activity',
            'NOAA scientists increased predicted named storms to 19, citing exceptionally warm sea-surface temperatures and fading El Niño conditions that reduce wind shear in the main development region.',
            [
                'Emergency managers urged Gulf Coast residents to finalize evacuation plans early. Reinsurers adjusted catastrophe models upward.',
                'Climate attribution studies link warming oceans to rapid intensification trends observed in recent seasons.',
            ],
            ['hurricane', 'NOAA', 'forecast', 'Atlantic'],
            4, 10, 8900,
            image_index=0,
            extra_categories=['environment'],
        ),
        _article(
            'weather',
            'Record heatwave scorches South Asia, closing schools in multiple states',
            'Temperatures surpassed 45°C in parts of India and Pakistan, straining power grids and hospital admissions for heatstroke, as meteorologists warned the dome could persist two more weeks.',
            [
                'Authorities opened cooling centres and adjusted outdoor labour restrictions. Farmers reported wilt damage to wheat and vegetable crops.',
                'Long-term adaptation plans include reflective roofing programmes and urban tree canopy expansion.',
            ],
            ['heatwave', 'South Asia', 'climate', 'public health'],
            5, 42, 2400,
            image_index=1,
        ),
        _article(
            'weather',
            'Atmospheric river brings flooding to Pacific Northwest after drought',
            'A series of moisture-laden systems dropped month\'s worth of rain on Oregon and Washington within days, triggering mudslides and reservoir management challenges.',
            [
                'Hydrologists said saturated soils increased landslide susceptibility in burn-scar regions. Ski resorts welcomed deep snowpack recovery.',
                'Infrastructure crews inspected levees upgraded after 2023 flood events.',
            ],
            ['atmospheric river', 'flooding', 'Pacific Northwest', 'rain'],
            0, 130, 1100,
            image_index=2,
        ),
        _article(
            'weather',
            'Met Office issues first purple extreme heat warning for southern England',
            'The new top-tier alert covers London and surrounding counties with projected overnight lows failing to drop below 25°C, elevating mortality risk for elderly residents.',
            [
                'Hospitals activated surge staffing for emergency departments. Transport operators imposed speed restrictions on rail lines vulnerable to buckling.',
                'Climate scientists said such warnings may become annual occurrences without aggressive mitigation.',
            ],
            ['heat warning', 'Met Office', 'United Kingdom', 'extreme weather'],
            1, 290, 620,
            image_index=3,
        ),
    ]


def _video() -> list[dict]:
    return [
        _article(
            'video',
            'On the ground: Inside the evacuation corridors of Port Meridian',
            'Our correspondents spent 72 hours documenting civilian departures through a humanitarian corridor in Port Meridian, capturing stories of families separated at checkpoints and aid workers rationing medical supplies.',
            [
                'Video footage verified by editorial geolocation teams shows queue lengths exceeding four kilometres at dawn. International observers called for extended ceasefire windows.',
                'Viewer discretion is advised for sequences filmed near field hospitals along the southern route.',
            ],
            ['documentary', 'conflict', 'humanitarian', 'correspondent'],
            2, 2, 27500,
            image_index=0,
            extra_categories=['breaking_news', 'world'],
            video_url='https://www.youtube.com/watch?v=L_LUpnjgPso',
        ),
        _article(
            'video',
            'Exclusive footage reveals scale of glacier collapse in Arctic research zone',
            'Drone operators contracted by a Nevox film unit recorded a seven-kilometre ice shelf disintegration over 48 hours, providing scientists rare continuous imagery for climate models.',
            [
                'Glaciologists interviewed in the piece say the event released freshwater equivalent to a month of London consumption.',
                'The full 12-minute report includes thermal imaging overlays and interviews from the Norwegian Polar Institute.',
            ],
            ['glacier', 'Arctic', 'climate', 'drone footage'],
            3, 7, 22100,
            image_index=1,
            extra_categories=['environment', 'science'],
            video_url='https://www.youtube.com/watch?v=OX9LcbQamYo',
        ),
        _article(
            'video',
            'Match point: Behind-the-scenes of the longest Wimbledon final in history',
            'Mic\'d-up cameras followed both finalists through changeovers and locker-room intervals during a five-set marathon that stretched past midnight on Centre Court.',
            [
                'The broadcast drew the highest streaming numbers in tournament history, according to All England Club data.',
                'Coaches discuss hydration strategies and mental reset rituals rarely visible to television audiences.',
            ],
            ['Wimbledon', 'tennis', 'sports documentary', 'behind the scenes'],
            4, 15, 19400,
            image_index=2,
            extra_categories=['sports'],
        ),
        _article(
            'video',
            'Tech demo: How autonomous tractors are reshaping Midwest harvest season',
            'Farmers in Iowa allowed Nevox cameras aboard cab-less planters synchronizing via satellite guidance, illustrating labour savings and data-driven planting precision.',
            [
                'Union organisers raise questions about rural job displacement and repair monopolies on proprietary software.',
                'Manufacturers claim fuel efficiency improvements up to 12% from optimized path planning.',
            ],
            ['agriculture', 'autonomous vehicles', 'technology', 'Midwest'],
            5, 240, 1600,
            image_index=3,
            extra_categories=['technology'],
        ),
    ]


_CATEGORY_BUILDERS = [
    _breaking_news,
    _world,
    _politics,
    _business,
    _economy,
    _technology,
    _science,
    _health,
    _sports,
    _entertainment,
    _culture,
    _lifestyle,
    _opinion,
    _education,
    _environment,
    _crime,
    _travel,
    _food,
    _real_estate,
    _weather,
    _video,
]


def get_all_articles() -> list[dict]:
    articles: list[dict] = []
    for builder in _CATEGORY_BUILDERS:
        articles.extend(builder())
    return articles
