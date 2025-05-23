<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Career Path Advisor</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f0f2f5;
        }
        .timer-animation {
            transition: width 1s linear;
        }
        .option.selected {
            border-color: #3b82f6;
            background-color: #eff6ff;
        }
        .career-card {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .career-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
    </style>
</head>
<body class="min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <!-- Header -->
        <header class="text-center mb-8">
            <h1 class="text-3xl font-bold text-gray-800 mb-2">Career Path Advisor</h1>
            <p class="text-gray-600">Discover your ideal career path through our AI-powered assessment</p>
        </header>

        <!-- Welcome Screen (Initially Visible) -->
        <div id="welcomeScreen" class="bg-white rounded-lg shadow-md p-8 mb-8 text-center">
            <div class="text-6xl text-blue-500 mb-4"><i class="bi bi-mortarboard-fill"></i></div>
            <h2 class="text-2xl font-bold text-gray-800 mb-4">Welcome to Your Career Journey</h2>
            <p class="text-gray-600 mb-6">This assessment will analyze your academic performance, interests, aptitudes, personality traits, and career values to recommend the best career paths for you.</p>
            <div class="mb-6 text-left bg-blue-50 p-4 rounded-lg">
                <h3 class="font-semibold text-lg mb-2">How It Works:</h3>
                <ul class="list-disc pl-5 space-y-2">
                    <li>You'll answer 30 questions (5 questions in each category)</li>
                    <li>Each question has a 60-second time limit</li>
                    <li>At the end, you'll receive personalized career recommendations</li>
                </ul>
            </div>
            <button id="startAssessment" class="bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 transition">
                Start My Assessment
            </button>
        </div>

        <!-- Question Section (Initially Hidden) -->
        <div id="questionContainer" class="bg-white rounded-lg shadow-md p-6 mb-8 hidden">
            <!-- Timer -->
            <div class="mb-4">
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                    <div id="timer" class="bg-blue-600 h-2.5 rounded-full timer-animation" style="width: 100%"></div>
                </div>
                <p class="text-sm text-gray-600 mt-1">Time remaining: <span id="timeLeft">60</span> seconds</p>
            </div>

            <!-- Progress -->
            <div class="mb-6">
                <div class="flex justify-between text-sm text-gray-600 mb-1">
                    <span>Progress</span>
                    <span id="progress">1/30</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                    <div id="progressBar" class="bg-green-500 h-2.5 rounded-full" style="width: 3.33%"></div>
                </div>
            </div>

            <!-- Category Badge -->
            <div class="mb-4">
                <span id="categoryBadge" class="inline-block bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                    Academic Performance
                </span>
            </div>

            <!-- Question -->
            <div id="questionText" class="text-xl font-semibold mb-6">
                How would you rate your academic performance in Mathematics?
            </div>

            <!-- Options -->
            <div id="options" class="space-y-3">
                <button class="w-full text-left p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition option">
                    Excellent (Above 90%)
                </button>
                <button class="w-full text-left p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition option">
                    Good (70-90%)
                </button>
                <button class="w-full text-left p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition option">
                    Average (50-70%)
                </button>
                <button class="w-full text-left p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition option">
                    Below Average (Below 50%)
                </button>
            </div>
        </div>

        <!-- Analysis In Progress (Initially Hidden) -->
        <div id="analysisInProgress" class="bg-white rounded-lg shadow-md p-8 mb-8 text-center hidden">
            <div class="animate-spin text-5xl text-blue-500 mb-6">
                <i class="bi bi-gear-wide-connected"></i>
            </div>
            <h2 class="text-2xl font-bold text-gray-800 mb-3">Analyzing Your Responses</h2>
            <p class="text-gray-600 mb-4">Our AI is processing your answers to generate personalized recommendations...</p>
            <div class="w-full bg-gray-200 rounded-full h-2.5 mb-4">
                <div id="analysisProgress" class="bg-blue-600 h-2.5 rounded-full" style="width: 0%"></div>
            </div>
            <p class="text-sm text-gray-500">This will take just a moment</p>
        </div>

        <!-- Results Section (Initially Hidden) -->
        <div id="resultsContainer" class="hidden">
            <div class="bg-white rounded-lg shadow-md p-6 mb-8">
                <div class="text-center mb-6">
                    <div class="inline-block p-3 rounded-full bg-green-100 text-green-500 text-4xl mb-3">
                        <i class="bi bi-check-circle-fill"></i>
                    </div>
                    <h2 class="text-2xl font-bold text-gray-800">Your Career Assessment Results</h2>
                    <p class="text-gray-600">Based on your responses, we've analyzed your profile and identified ideal career paths</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                    <!-- Strength Analysis -->
                    <div class="bg-gray-50 rounded-lg p-6">
                        <h3 class="text-lg font-semibold mb-4">Your Strengths Profile</h3>
                        <canvas id="strengthsChart" height="250"></canvas>
                    </div>

                    <!-- Career Match -->
                    <div class="bg-gray-50 rounded-lg p-6">
                        <h3 class="text-lg font-semibold mb-4">Career Match Analysis</h3>
                        <canvas id="careerMatchChart" height="250"></canvas>
                    </div>
                </div>

                <!-- Category Breakdown -->
                <div class="mb-8">
                    <h3 class="text-lg font-semibold mb-4">Your Assessment Breakdown</h3>
                    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                        <div class="bg-blue-50 p-4 rounded-lg">
                            <div class="flex justify-between items-center mb-2">
                                <h4 class="font-medium">Academic Performance</h4>
                                <span id="academicScore" class="text-blue-700 font-semibold">85%</span>
                            </div>
                            <p class="text-sm text-gray-600">Strong in mathematics and sciences</p>
                        </div>
                        <div class="bg-purple-50 p-4 rounded-lg">
                            <div class="flex justify-between items-center mb-2">
                                <h4 class="font-medium">Interests</h4>
                                <span id="interestsScore" class="text-purple-700 font-semibold">90%</span>
                            </div>
                            <p class="text-sm text-gray-600">Investigative and conventional</p>
                        </div>
                        <div class="bg-green-50 p-4 rounded-lg">
                            <div class="flex justify-between items-center mb-2">
                                <h4 class="font-medium">Aptitude</h4>
                                <span id="aptitudeScore" class="text-green-700 font-semibold">75%</span>
                            </div>
                            <p class="text-sm text-gray-600">Logical reasoning and problem-solving</p>
                        </div>
                        <div class="bg-yellow-50 p-4 rounded-lg">
                            <div class="flex justify-between items-center mb-2">
                                <h4 class="font-medium">Personality</h4>
                                <span id="personalityScore" class="text-yellow-700 font-semibold">80%</span>
                            </div>
                            <p class="text-sm text-gray-600">Analytical and detail-oriented</p>
                        </div>
                        <div class="bg-red-50 p-4 rounded-lg">
                            <div class="flex justify-between items-center mb-2">
                                <h4 class="font-medium">Career Values</h4>
                                <span id="valuesScore" class="text-red-700 font-semibold">95%</span>
                            </div>
                            <p class="text-sm text-gray-600">Values stability and growth potential</p>
                        </div>
                        <div class="bg-indigo-50 p-4 rounded-lg">
                            <div class="flex justify-between items-center mb-2">
                                <h4 class="font-medium">External Factors</h4>
                                <span id="externalScore" class="text-indigo-700 font-semibold">70%</span>
                            </div>
                            <p class="text-sm text-gray-600">Market demand and family influence</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Top Career Recommendations -->
            <div class="bg-white rounded-lg shadow-md p-6 mb-8">
                <h2 class="text-xl font-semibold mb-6">Your Top Career Recommendations</h2>
                <div class="space-y-6" id="careerRecommendations">
                    <!-- Career cards will be inserted here -->
                </div>
            </div>

            <!-- Recommended Courses -->
            <div class="bg-white rounded-lg shadow-md p-6 mb-8">
                <h2 class="text-xl font-semibold mb-4">Recommended Courses & Education Paths</h2>
                <div class="space-y-4" id="courseRecommendations">
                    <!-- Course recommendations will be inserted here -->
                </div>
            </div>

            <!-- Next Steps -->
            <div class="bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg shadow-md p-6 text-white">
                <h2 class="text-xl font-semibold mb-4">Next Steps in Your Career Journey</h2>
                <ul class="space-y-3 mb-6">
                    <li class="flex items-start">
                        <i class="bi bi-check-circle-fill mr-2 mt-1"></i>
                        <span>Research the recommended career paths to understand day-to-day responsibilities</span>
                    </li>
                    <li class="flex items-start">
                        <i class="bi bi-check-circle-fill mr-2 mt-1"></i>
                        <span>Connect with professionals in your fields of interest for informational interviews</span>
                    </li>
                    <li class="flex items-start">
                        <i class="bi bi-check-circle-fill mr-2 mt-1"></i>
                        <span>Explore suggested courses and educational requirements</span>
                    </li>
                    <li class="flex items-start">
                        <i class="bi bi-check-circle-fill mr-2 mt-1"></i>
                        <span>Consider seeking guidance from career counselors at your school</span>
                    </li>
                </ul>
                <button class="bg-white text-blue-600 py-2 px-4 rounded-lg font-medium hover:bg-blue-50 transition" onclick="window.print()">
                    <i class="bi bi-printer"></i> Print Your Results
                </button>
            </div>
        </div>
    </div>

    <script>
        // Global variables
        let currentQuestion = 1;
        const totalQuestions = 30;
        let timer;
        let selectedOption = null;
        let scores = {
            academic: 0,
            interests: 0,
            aptitude: 0,
            personality: 0,
            values: 0,
            external: 0
        };

        // Questions database
        const questions = [
            // Academic Performance (1-5)
            {
                text: "How would you rate your academic performance in Mathematics?",
                category: "academic",
                categoryDisplay: "Academic Performance",
                options: [
                    "Excellent (Above 90%)",
                    "Good (70-90%)",
                    "Average (50-70%)",
                    "Below Average (Below 50%)"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How would you rate your academic performance in Science subjects?",
                category: "academic",
                categoryDisplay: "Academic Performance",
                options: [
                    "Excellent (Above 90%)",
                    "Good (70-90%)",
                    "Average (50-70%)",
                    "Below Average (Below 50%)"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How would you rate your academic performance in Language & Literature?",
                category: "academic",
                categoryDisplay: "Academic Performance",
                options: [
                    "Excellent (Above 90%)",
                    "Good (70-90%)",
                    "Average (50-70%)",
                    "Below Average (Below 50%)"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How would you rate your academic performance in Social Studies/Humanities?",
                category: "academic",
                categoryDisplay: "Academic Performance",
                options: [
                    "Excellent (Above 90%)",
                    "Good (70-90%)",
                    "Average (50-70%)",
                    "Below Average (Below 50%)"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How would you rate your performance in creative subjects (Art, Music, etc.)?",
                category: "academic",
                categoryDisplay: "Academic Performance",
                options: [
                    "Excellent (Above 90%)",
                    "Good (70-90%)",
                    "Average (50-70%)",
                    "Below Average (Below 50%)"
                ],
                scores: [4, 3, 2, 1]
            },
            // Interests Assessment (6-10)
            {
                text: "How much do you enjoy solving complex problems or puzzles?",
                category: "interests",
                categoryDisplay: "Interest Assessment",
                options: [
                    "Very much - I seek them out",
                    "I enjoy them moderately",
                    "I'm neutral about them",
                    "I prefer to avoid them"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How interested are you in creative activities like writing, art, or design?",
                category: "interests",
                categoryDisplay: "Interest Assessment",
                options: [
                    "Extremely interested",
                    "Moderately interested",
                    "Slightly interested",
                    "Not interested at all"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How do you feel about working with technology and computers?",
                category: "interests",
                categoryDisplay: "Interest Assessment",
                options: [
                    "I love technology and always want to learn more",
                    "I'm comfortable using technology",
                    "I use technology when necessary",
                    "I prefer to avoid technology when possible"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How interested are you in helping or teaching others?",
                category: "interests",
                categoryDisplay: "Interest Assessment",
                options: [
                    "Very interested - it's my passion",
                    "Moderately interested",
                    "Somewhat interested",
                    "Not particularly interested"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How do you feel about leadership roles and influencing others?",
                category: "interests",
                categoryDisplay: "Interest Assessment",
                options: [
                    "I naturally take leadership roles",
                    "I'm comfortable leading when needed",
                    "I occasionally enjoy leadership",
                    "I prefer to follow rather than lead"
                ],
                scores: [4, 3, 2, 1]
            },
            // Aptitude Testing (11-15)
            {
                text: "How easily do you learn new technical skills?",
                category: "aptitude",
                categoryDisplay: "Aptitude Testing",
                options: [
                    "Very easily - I pick up new skills quickly",
                    "Fairly easily with some practice",
                    "With considerable effort and time",
                    "I struggle to learn technical skills"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How would you rate your problem-solving abilities?",
                category: "aptitude",
                categoryDisplay: "Aptitude Testing",
                options: [
                    "Excellent - I can solve most problems efficiently",
                    "Good - I can usually find solutions",
                    "Average - I solve some problems",
                    "Below average - I often struggle with problems"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How would you rate your verbal communication skills?",
                category: "aptitude",
                categoryDisplay: "Aptitude Testing",
                options: [
                    "Excellent - I communicate clearly and persuasively",
                    "Good - I'm an effective communicator",
                    "Average - I get my point across",
                    "Below average - I sometimes struggle to express myself"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How would you rate your ability to think critically and analyze information?",
                category: "aptitude",
                categoryDisplay: "Aptitude Testing",
                options: [
                    "Excellent - I thoroughly analyze and evaluate information",
                    "Good - I can identify patterns and draw conclusions",
                    "Average - I understand basic analysis",
                    "Below average - I find analysis challenging"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How would you rate your creativity and ability to generate new ideas?",
                category: "aptitude",
                categoryDisplay: "Aptitude Testing",
                options: [
                    "Highly creative - I constantly generate new ideas",
                    "Moderately creative - I have good ideas sometimes",
                    "Somewhat creative in specific areas",
                    "I prefer following established methods"
                ],
                scores: [4, 3, 2, 1]
            },
            // Personality Analysis (16-20)
            {
                text: "How do you typically approach new tasks or projects?",
                category: "personality",
                categoryDisplay: "Personality Analysis",
                options: [
                    "I plan thoroughly before starting",
                    "I create a basic plan and adjust as needed",
                    "I prefer to dive in and learn as I go",
                    "I take direction from others on how to proceed"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "In group settings, how do you typically interact?",
                category: "personality",
                categoryDisplay: "Personality Analysis",
                options: [
                    "I naturally take charge and direct the group",
                    "I actively contribute ideas and opinions",
                    "I participate when I have something valuable to add",
                    "I prefer to listen and follow along"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How do you handle stress and pressure?",
                category: "personality",
                categoryDisplay: "Personality Analysis",
                options: [
                    "I thrive under pressure and perform better",
                    "I remain calm and focused under most pressure",
                    "I can manage stress but prefer to avoid it",
                    "I find stress and pressure difficult to handle"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How do you approach working with details?",
                category: "personality",
                categoryDisplay: "Personality Analysis",
                options: [
                    "I'm very detail-oriented and thorough",
                    "I pay attention to important details",
                    "I focus on the big picture more than details",
                    "I often overlook details in favor of speed"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How do you prefer to make decisions?",
                category: "personality",
                categoryDisplay: "Personality Analysis",
                options: [
                    "Based on logical analysis and facts",
                    "Balancing logic with intuition",
                    "Based on feelings and values",
                    "I prefer others to make decisions"
                ],
                scores: [4, 3, 2, 1]
            },
            // Career Values (21-25)
            {
                text: "How important is income potential in your career choice?",
                category: "values",
                categoryDisplay: "Career Values",
                options: [
                    "Extremely important - a top priority",
                    "Very important, but balanced with other factors",
                    "Somewhat important",
                    "Not very important compared to other factors"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How important is work-life balance in your career choice?",
                category: "values",
                categoryDisplay: "Career Values",
                options: [
                    "Extremely important - a top priority",
                    "Very important, but balanced with other factors",
                    "Somewhat important",
                    "Not very important compared to other factors"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How important is job security in your career choice?",
                category: "values",
                categoryDisplay: "Career Values",
                options: [
                    "Extremely important - a top priority",
                    "Very important, but balanced with other factors",
                    "Somewhat important",
                    "Not very important compared to other factors"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How important is making a positive social impact in your career choice?",
                category: "values",
                categoryDisplay: "Career Values",
                options: [
                    "Extremely important - a top priority",
                    "Very important, but balanced with other factors",
                    "Somewhat important",
                    "Not very important compared to other factors"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How important is continuous learning and growth in your career choice?",
                category: "values",
                categoryDisplay: "Career Values",
                options: [
                    "Extremely important - a top priority",
                    "Very important, but balanced with other factors",
                    "Somewhat important",
                    "Not very important compared to other factors"
                ],
                scores: [4, 3, 2, 1]
            },
            // External Factors (26-30)
            {
                text: "How much does your family influence your career decisions?",
                category: "external",
                categoryDisplay: "External Factors",
                options: [
                    "Significantly - their opinion is very important",
                    "Moderately - I consider their input",
                    "Slightly - I listen but make my own decisions",
                    "Not at all - I decide independently"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How important is market demand and job availability in your career choice?",
                category: "external",
                categoryDisplay: "External Factors",
                options: [
                    "Extremely important - I choose based on demand",
                    "Very important, but balanced with my interests",
                    "Somewhat important",
                    "Not very important compared to my passion"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How willing are you to relocate for career opportunities?",
                category: "external",
                categoryDisplay: "External Factors",
                options: [
                    "Very willing - I'll go wherever opportunities exist",
                    "Moderately willing - within my country/region",
                    "Somewhat willing - within my city/state",
                    "Not willing - I need to stay in my current location"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How much do you consider future industry trends in your career planning?",
                category: "external",
                categoryDisplay: "External Factors",
                options: [
                    "Extensively - I research future trends thoroughly",
                    "Considerably - I'm aware of major trends",
                    "Somewhat - I have basic awareness",
                    "Minimally - I focus on current opportunities"
                ],
                scores: [4, 3, 2, 1]
            },
            {
                text: "How important is prestige or social status in your career choice?",
                category: "external",
                categoryDisplay: "External Factors",
                options: [
                    "Extremely important - a top priority",
                    "Very important, but balanced with other factors",
                    "Somewhat important",
                    "Not very important compared to other factors"
                ],
                scores: [4, 3, 2, 1]
            }
        ];

        // Career recommendations based on scores
        const careerRecommendations = [
            {
                title: "Software Engineering",
                description: "Design, development, and maintenance of software systems and applications.",
                matchCriteria: {
                    academic: 75,
                    interests: 80,
                    aptitude: 80,
                    personality: 70,
                    values: 70,
                    external: 90
                },
                courses: [
                    "Computer Science",
                    "Software Engineering",
                    "Information Technology",
                    "Computer Engineering"
                ],
                skills: ["Programming", "Problem-solving", "Technical design", "Teamwork"],
                outlook: "Excellent growth potential with high demand across industries",
                icon: "bi-code-slash"
            },
            {
                title: "Data Science",
                description: "Analysis of data to extract meaningful insights and support decision-making.",
                matchCriteria: {
                    academic: 85,
                    interests: 75,
                    aptitude: 85,
                    personality: 80,
                    values: 70,
                    external: 90
                },
                courses: [
                    "Data Science",
                    "Statistics",
                    "Computer Science with Data Analytics",
                    "Mathematics with Computing"
                ],
                skills: ["Statistical analysis", "Programming", "Data visualization", "Critical thinking"],
                outlook: "Rapidly growing field with opportunities across sectors",
                icon: "bi-graph-up"
            },
            {
                title: "UX/UI Design",
                description: "Creating user-friendly interfaces and optimizing user experiences for digital products.",
                matchCriteria: {
                    academic: 70,
                    interests: 85,
                    aptitude: 75,
                    personality: 80,
                    values: 75,
                    external: 85
                },
                courses: [
                    "User Experience Design",
                    "Interaction Design",
                    "Digital Media Design",
                    "Human-Computer Interaction"
                ],
                skills: ["Visual design", "User research", "Prototyping", "Empathy"],
                outlook: "Growing demand as businesses focus on user experience",
                icon: "bi-palette"
            },
            {
                title: "Healthcare Professional",
                description: "Providing medical care and promoting health and wellness.",
                matchCriteria: {
                    academic: 80,
                    interests: 75,
                    aptitude: 70,
                    personality: 85,
                    values: 90,
                    external: 85
                },
                courses: [
                    "Medicine",
                    "Nursing",
                    "Healthcare Management",
                    "Biomedical Science"
                ],
                skills: ["Patient care", "Clinical knowledge", "Communication", "Empathy"],
                outlook: "Stable career with consistent demand and meaningful impact",
                icon: "bi-heart-pulse"
            },
            {
                title: "Financial Analyst",
                description: "Analysis of financial data to guide business and investment decisions.",
                matchCriteria: {
                    academic: 80,
                    interests: 70,
                    aptitude: 85,
                    personality: 75,
                    values: 80,
                    external: 85
                },
                courses: [
                    "Finance",
                    "Economics",
                    "Accounting",
                    "Business Administration"
                ],
                skills: ["Financial modeling", "Data analysis", "Risk assessment", "Attention to detail"],
                outlook: "Steady demand with opportunities for specialization",
                icon: "bi-cash-coin"
            },
            {
                title: "Marketing Specialist",
                description: "Developing and implementing strategies to promote products and services.",
                matchCriteria: {
                    academic: