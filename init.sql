-- Enable pgvector extension for vector operations
CREATE EXTENSION IF NOT EXISTS vector;

-- Create students table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    student_id TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create assignments table
CREATE TABLE IF NOT EXISTS assignments (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    original_text TEXT,
    topic TEXT,
    academic_level TEXT,
    word_count INTEGER,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create analysis_results table
CREATE TABLE IF NOT EXISTS analysis_results (
    id SERIAL PRIMARY KEY,
    assignment_id INTEGER REFERENCES assignments(id) ON DELETE CASCADE,
    suggested_sources JSONB,
    plagiarism_score FLOAT,
    flagged_sections JSONB,
    research_suggestions TEXT,
    citation_recommendations TEXT,
    confidence_score FLOAT,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create academic_sources table for RAG
CREATE TABLE IF NOT EXISTS academic_sources (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT NOT NULL,
    publication_year INTEGER,
    abstract TEXT,
    full_text TEXT,
    source_type TEXT CHECK (source_type IN ('paper', 'textbook', 'course_material')),
    embedding VECTOR(1536), -- OpenAI text-embedding-ada-002 dimension
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_assignments_student_id ON assignments(student_id);
CREATE INDEX IF NOT EXISTS idx_analysis_results_assignment_id ON analysis_results(assignment_id);
CREATE INDEX IF NOT EXISTS idx_academic_sources_source_type ON academic_sources(source_type);
CREATE INDEX IF NOT EXISTS idx_academic_sources_embedding ON academic_sources USING ivfflat (embedding vector_cosine_ops);

-- Insert sample academic sources for testing
INSERT INTO academic_sources (title, authors, publication_year, abstract, full_text, source_type) VALUES
('Machine Learning in Education: A Comprehensive Review', 'Dr. Sarah Johnson, Prof. Michael Chen', 2023, 'This paper explores the applications of machine learning in educational settings, focusing on personalized learning and assessment methods.', 'Machine learning has revolutionized the field of education by enabling personalized learning experiences, automated assessment systems, and intelligent tutoring platforms. This comprehensive review examines various ML techniques applied in educational contexts, including natural language processing for essay evaluation, recommendation systems for course content, and predictive analytics for student performance. The paper discusses both the benefits and challenges of implementing ML in education, with particular attention to ethical considerations and data privacy concerns.', 'paper'),
('Introduction to Academic Writing', 'Dr. Emily Rodriguez', 2022, 'A foundational guide to academic writing principles, structure, and citation methods.', 'Academic writing is a formal style of writing used in universities and scholarly publications. It is characterized by clear, concise language, logical structure, and proper citation of sources. This guide covers essential elements including thesis statements, argument development, evidence integration, and various citation styles such as APA, MLA, and Chicago. The text emphasizes the importance of critical thinking, original analysis, and ethical research practices in academic work.', 'textbook'),
('Research Methodology in Computer Science', 'Prof. David Kim, Dr. Lisa Wang', 2023, 'Comprehensive guide to research methods and experimental design in computer science.', 'This course material provides an in-depth exploration of research methodologies specific to computer science. Topics include experimental design, statistical analysis, literature review techniques, and research ethics. The material covers both quantitative and qualitative research approaches, with practical examples from software engineering, artificial intelligence, and data science domains. Students will learn to design rigorous experiments, analyze results, and present findings in academic contexts.', 'course_material'),
('Plagiarism Detection: Algorithms and Applications', 'Dr. Robert Taylor', 2021, 'Technical analysis of plagiarism detection algorithms and their implementation in academic settings.', 'This paper presents a detailed analysis of various algorithms used for plagiarism detection in academic writing. The study compares text similarity algorithms, including n-gram analysis, semantic similarity measures, and machine learning approaches. The research evaluates the effectiveness of different detection methods across various types of academic content, from essays to research papers. Key findings include recommendations for optimal algorithm selection based on content type and detection requirements.', 'paper'),
('Database Systems: Design and Implementation', 'Prof. Maria Garcia, Dr. James Wilson', 2022, 'Comprehensive textbook covering database design principles and implementation techniques.', 'This textbook provides a thorough introduction to database systems, covering both theoretical foundations and practical implementation. Topics include relational database design, SQL programming, transaction management, and database optimization. The book includes numerous examples and exercises to help students understand complex concepts. Special attention is given to modern database technologies, including NoSQL databases, cloud-based solutions, and big data processing frameworks.', 'textbook');

-- Create a function to calculate cosine similarity
CREATE OR REPLACE FUNCTION cosine_similarity(a vector, b vector) 
RETURNS float AS $$
BEGIN
    RETURN 1 - (a <=> b);
END;
$$ LANGUAGE plpgsql IMMUTABLE STRICT;


