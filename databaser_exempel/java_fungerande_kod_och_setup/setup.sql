-- Blandning av tables, views, inserts

-- Tables -------------------------------------------------------------

CREATE TABLE Programs (
    name TEXT PRIMARY KEY NOT NULL,
    abbreviation TEXT
);

CREATE TABLE Students (
    idnr CHAR(10) PRIMARY KEY NOT NULL, 
    name TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    program TEXT NOT NULL,
    UNIQUE (idnr, program),
    FOREIGN KEY (program) REFERENCES Programs(name)
);

CREATE TABLE Branches (
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    PRIMARY KEY (name, program) -- two primary keys
    -- CONSTRAINT none sense CHECK (area >population * 10) );
);

CREATE TABLE Courses (
    code CHAR(6) PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    credits INT NOT NULL CHECK (credits >= 0), -- or DEAFULT 0,
    department TEXT NOT NULL
);

-- Only courses from all Courses kan exist here -> Foreign keys
CREATE TABLE LimitedCourses (
    code CHAR(6) PRIMARY KEY NOT NULL,
    capacity INT NOT NULL CHECK (capacity > -1),
    FOREIGN KEY (code) REFERENCES Courses(code)
);

CREATE TABLE StudentBranches(
    student CHAR(10) NOT NULL,
    branch TEXT NOT NULL,
    program TEXT NOT NULL,
    PRIMARY KEY (student),
    FOREIGN KEY (program, student) REFERENCES Students(program, idnr),
    FOREIGN KEY (branch, program) REFERENCES Branches(name, program)
   
);

CREATE TABLE Classifications(
    name TEXT PRIMARY KEY NOT NULL
);

CREATE TABLE Classified (
    course CHAR(6) NOT NULL,
    classification TEXT NOT NULL,
    PRIMARY KEY (course, classification),
    FOREIGN KEY (course) REFERENCES Courses (code),
    FOREIGN KEY (classification) REFERENCES Classifications (name)
);

CREATE TABLE MandatoryProgram(
    course CHAR(6) NOT NULL,
    program TEXT NOT NULL,
    PRIMARY KEY (program, course),
    FOREIGN KEY (course) REFERENCES Courses(code)    
);

CREATE TABLE MandatoryBranch(
    course CHAR(6),
    branch TEXT NOT NULL,  
    program TEXT NOT NULL, 
    PRIMARY KEY (course, branch, program),
    FOREIGN KEY (course) REFERENCES Courses(code),
    FOREIGN KEY (branch, program) REFERENCES Branches(name, program)   
);

-- Alla studenters kurser de är registrerade på
CREATE TABLE Registered (
    student CHAR(10) NOT NULL,
    course CHAR(6) NOT NULL,
    PRIMARY KEY (student, course), 
    FOREIGN KEY (student) REFERENCES Students(idnr),
    FOREIGN KEY (course) REFERENCES Courses(code)
);

CREATE TABLE Taken (
    student CHAR(10) NOT NULL,
    course CHAR(6) NOT NULL,
    grade CHAR(1) NOT NULL CHECK (grade IN ('U','3','4','5')),
    PRIMARY KEY (student, course), -- Ett betyg per student och kurs
    FOREIGN KEY (student) REFERENCES Students(idnr),
    FOREIGN KEY (course) REFERENCES Courses(code)
    --CONSTRAINT okgrade CHECK (grade IN (3,4,5))
);

CREATE TABLE WaitingList(
    student char(10) NOT NULL,
    course CHAR(6) NOT NULL,
    position INT NOT NULL, 
    UNIQUE (course, position),
    PRIMARY KEY(student, course),
    FOREIGN KEY(student) REFERENCES Students(idnr),
    FOREIGN KEY(course) REFERENCES LimitedCourses(code)
);

CREATE TABLE RecommendedBranch (
    course CHAR(6) NOT NULL,
    branch TEXT NOT NULL,
    program TEXT NOT NULL,
    PRIMARY KEY (course, branch, program),
    FOREIGN KEY (course) REFERENCES Courses(code),
    FOREIGN KEY (branch, program) REFERENCES Branches(name, program)
);

CREATE TABLE Departments (
  name TEXT PRIMARY KEY NOT NULL,
  abbreviation TEXT UNIQUE NOT NULL
);

CREATE TABLE DepartmentProgram (
    department TEXT NOT NULL,
    program TEXT NOT NULL,
    PRIMARY KEY (department, program),
    FOREIGN KEY (department) REFERENCES Departments(name),
    FOREIGN KEY (program) REFERENCES Programs(name)
);

CREATE TABLE DepartmentCourses (
    department TEXT NOT NULL,
    course TEXT PRIMARY KEY NOT NULL,
    FOREIGN KEY (department) REFERENCES Departments(name),
    FOREIGN KEY (course) REFERENCES Courses(code)
);

CREATE TABLE Prerequisite (
    course CHAR(6) NOT NULL,
    prerequisite CHAR(6) NOT NULL,
    PRIMARY KEY (course, prerequisite),
    FOREIGN KEY (course) REFERENCES Courses(code),
    FOREIGN KEY (prerequisite) REFERENCES Courses(code)
);

-- Views -------------------------------------------------------------

-- BasicInformation(idnr, name, login, program, branch)
CREATE VIEW BasicInformation AS (
    SELECT 
    Students.idnr,      -- för att förtydliga vilken idnr man menar, behövs egentligen inte här då tex idnr inte finns i StudentBranches 
    Students.name,
    Students.login,
    Students.program,
    StudentBranches.branch
    FROM Students LEFT OUTER JOIN StudentBranches ON idnr = student -- branch can be empty
);

-- FinishedCourses(student, course, grade, credits)
-- Cross product
CREATE VIEW FinishedCourses AS (
    SELECT
    Taken.student, -- bara studenter som är finished
    Taken.course,
    Taken.grade,
    Courses.credits
    FROM Students -- ger ändå bara finished students
    JOIN Taken ON idnr = student -- Taken has multiple students? -> cross product
    JOIN Courses ON code = course -- code from Courses, course from Taken
    -- cross join fungerar inte?
);

-- PassedCourses(student, course, credits)
-- 
CREATE VIEW PassedCourses AS (
    SELECT
    student, -- vi skulle kunna skriva FinishedCourses.student
    course,
    credits -- gick inte att ha kvar Taken.credits osv EFTERSOM VI SKRIVER ANDVÄNDER FROM FINISHEDCOURSES
    FROM FinishedCourses WHERE grade != 'U'
);

-- Registrations(student, course, status)
CREATE VIEW Registrations AS (
    SELECT
    Registered.student, -- inte nödvänigt med AS här?
    Registered.course,
    'registered' AS status FROM Registered  
    UNION
    SELECT
    WaitingList.student, -- kommer registered och waiting idnrs i samma kolumn?
    WaitingList.course,
    'waiting' AS status FROM WaitingList
);


CREATE VIEW MandatoryInProgram AS (
    SELECT
    BasicInformation.idnr AS student, -- för att få samma namn efter intersect
    MandatoryProgram.course AS course
    FROM BasicInformation JOIN MandatoryProgram ON BasicInformation.program = MandatoryProgram.program --idnr = student
);

CREATE VIEW MandatoryInBranch AS (
    SELECT
    BasicInformation.idnr AS student,
    MandatoryBranch.course AS course 
    FROM BasicInformation JOIN MandatoryBranch 
    ON BasicInformation.branch = MandatoryBranch.branch
    AND BasicInformation.program = MandatoryBranch.program -- different programs can have the same branch
);

CREATE VIEW MandatoryCourses AS (
    SELECT
    student,
    course
    FROM MandatoryInProgram
    UNION 
    SELECT
    student,
    course
    FROM MandatoryInBranch

);
CREATE VIEW UnreadMandatory AS (
    SELECT
    BasicInformation.idnr AS student, 
    MandatoryCourses.course AS course 
    FROM BasicInformation JOIN MandatoryCourses ON idnr = student      -- cross join fungerar inte
    EXCEPT
    SELECT
    student,
    course
    FROM PassedCourses
);

--  COALESCE(totalCredits.total, 0) AS totalCredits
CREATE VIEW TotalCredits AS (
    SELECT student,
    SUM(credits) AS totalCredits FROM PassedCourses  
    GROUP BY student -- summorna adderas för varje student
);

CREATE VIEW MandatoryLeft AS (
    SELECT
    student,
    COALESCE (COUNT(course), 0) as mandatoryLeft FROM UnreadMandatory 
    GROUP BY Student
);

CREATE VIEW MathCredits AS (
    SELECT
    student,
    COALESCE (SUM(credits), 0) as mathCredits FROM PassedCourses, Classified 
    WHERE PassedCourses.course = Classified.course
    AND Classified.classification = 'math'
    GROUP BY PassedCourses.student
);

CREATE VIEW ResearchCredits AS (
    SELECT
    student,
    COALESCE (SUM(credits), 0) as researchCredits FROM PassedCourses, Classified 
    WHERE PassedCourses.course = Classified.course
    AND Classified.classification = 'research'
    GROUP BY PassedCourses.student
);

CREATE VIEW SeminarCourses AS (
    SELECT
    student,
    COALESCE (COUNT(PassedCourses.course), 0) as seminarCourses FROM PassedCourses, Classified -- ambiguous
    WHERE PassedCourses.course = Classified.course
    AND Classified.classification = 'seminar'
    GROUP BY PassedCourses.student
);

CREATE VIEW RecommendedPassed AS (
  SELECT student, 
  PassedCourses.course, 
  PassedCourses.credits
  FROM PassedCourses
  JOIN BasicInformation ON PassedCourses.student = BasicInformation.idnr -- so we can use branch and program
  JOIN RecommendedBranch
  ON RecommendedBranch.course = PassedCourses.course 
  AND RecommendedBranch.branch = BasicInformation.branch
  AND RecommendedBranch.program = BasicInformation.program
);

CREATE VIEW RecommendedCredits AS (
  SELECT student, 
  SUM(credits) AS recommendedCredits
  FROM RecommendedPassed
  GROUP BY student
);

-- PathToGraduation(student, totalCredits, mandatoryLeft, mathCredits, researchCredits, seminarCourses, qualified)
CREATE VIEW PathToGraduation AS (
  SELECT
    BasicInformation.idnr AS student,
    COALESCE(totalCredits, 0) AS totalCredits,
    COALESCE(mandatoryLeft, 0) AS mandatoryLeft,
    COALESCE(mathCredits, 0) AS mathCredits,
    COALESCE(researchCredits, 0) AS researchCredits,
    COALESCE(seminarCourses, 0) AS seminarCourses,
  
  -- Qualified
    BasicInformation.branch IS NOT NULL
    AND COALESCE(mandatoryLeft, 0) = 0
    AND COALESCE(recommendedCredits, 0) >= 10
    AND COALESCE(mathCredits, 0) >= 20
    AND COALESCE(researchCredits, 0) >= 10
    AND COALESCE(seminarCourses, 0) > 0
    AS qualified
     
  FROM BasicInformation
  LEFT JOIN TotalCredits ON idnr = TotalCredits.student
  LEFT JOIN MandatoryLeft ON idnr = MandatoryLeft.student
  LEFT JOIN MathCredits ON idnr = MathCredits.student
  LEFT JOIN ResearchCredits ON idnr = ResearchCredits.student
  LEFT JOIN SeminarCourses ON idnr = SeminarCourses.student
  LEFT JOIN RecommendedCredits ON idnr = RecommendedCredits.student
);

-- Inserts -------------------------------------------------------------

INSERT INTO Branches VALUES ('B1','Prog1');
INSERT INTO Branches VALUES ('B2','Prog1');
INSERT INTO Branches VALUES ('B1','Prog2');

INSERT INTO Programs VALUES('Prog1', 'P1');
INSERT INTO Programs VALUES('Prog2', 'P2');
INSERT INTO Programs VALUES('Prog3', 'P3');

INSERT INTO Students VALUES ('1111111111','N1','ls1','Prog1');
INSERT INTO Students VALUES ('2222222222','N2','ls2','Prog1');
INSERT INTO Students VALUES ('3333333333','N3','ls3','Prog2');
INSERT INTO Students VALUES ('4444444444','N4','ls4','Prog1');
INSERT INTO Students VALUES ('5555555555','Nx','ls5','Prog2');
INSERT INTO Students VALUES ('6666666666','Nx','ls6','Prog2');
INSERT INTO Students VALUES ('7777777777','N7','ls7','Prog2'); -- new

-- Tests:
-- INSERT INTO Students values ('7777777777', 'N7', 'ls7', 'Prog3');
-- insert into branches values ('B1', 'Prog3');
-- INSERT INTO StudentBranches VALUES ('7777777777','B2','Prog3');

-- INSERT INTO Students values ('8888888888', 'N7', 'ls8', 'Prog2');
-- INSERT INTO StudentBranches VALUES ('8888888888','B1','Prog1');

INSERT INTO Courses VALUES ('CCC111','C1',22.5,'Dep1');
INSERT INTO Courses VALUES ('CCC222','C2',20,'Dep1');
INSERT INTO Courses VALUES ('CCC333','C3',30,'Dep1');
INSERT INTO Courses VALUES ('CCC444','C4',60,'Dep1');
INSERT INTO Courses VALUES ('CCC555','C5',50,'Dep1');
INSERT INTO Courses VALUES ('CCC666','C6',50,'Dep1');
INSERT INTO Courses VALUES ('CCC777','C7',50,'Dep1');

INSERT INTO LimitedCourses VALUES ('CCC222',1);
INSERT INTO LimitedCourses VALUES ('CCC333',2);
INSERT INTO LimitedCourses VALUES ('CCC555',1); -- new for lab 3
INSERT INTO LimitedCourses VALUES ('CCC666',1); -- new for lab 3
INSERT INTO LimitedCourses VALUES ('CCC777',1); -- new for lab 3

INSERT INTO Classifications VALUES ('math');
INSERT INTO Classifications VALUES ('research');
INSERT INTO Classifications VALUES ('seminar');

INSERT INTO Classified VALUES ('CCC333','math');
INSERT INTO Classified VALUES ('CCC444','math');
INSERT INTO Classified VALUES ('CCC444','research');
INSERT INTO Classified VALUES ('CCC444','seminar');


INSERT INTO StudentBranches VALUES ('2222222222','B1','Prog1');
INSERT INTO StudentBranches VALUES ('3333333333','B1','Prog2');
INSERT INTO StudentBranches VALUES ('4444444444','B1','Prog1');
INSERT INTO StudentBranches VALUES ('5555555555','B1','Prog2');

INSERT INTO MandatoryProgram VALUES ('CCC111','Prog1');

INSERT INTO MandatoryBranch VALUES ('CCC333', 'B1', 'Prog1');
INSERT INTO MandatoryBranch VALUES ('CCC444', 'B1', 'Prog2');

INSERT INTO RecommendedBranch VALUES ('CCC222', 'B1', 'Prog1');
INSERT INTO RecommendedBranch VALUES ('CCC333', 'B1', 'Prog2');

INSERT INTO Registered VALUES ('1111111111','CCC111');
INSERT INTO Registered VALUES ('1111111111','CCC222');
INSERT INTO Registered VALUES ('1111111111','CCC333');
-- INSERT INTO Registered VALUES ('2222222222','CCC222'); CCC222 is full
-- INSERT INTO Registered VALUES ('5555555555','CCC222'); CCC222 is full
INSERT INTO Registered VALUES ('5555555555','CCC333');

INSERT INTO Taken VALUES('4444444444','CCC111','5');
INSERT INTO Taken VALUES('4444444444','CCC222','5');
INSERT INTO Taken VALUES('4444444444','CCC333','5');
INSERT INTO Taken VALUES('4444444444','CCC444','5');

INSERT INTO Taken VALUES('5555555555','CCC111','5');
INSERT INTO Taken VALUES('5555555555','CCC222','4');
INSERT INTO Taken VALUES('5555555555','CCC444','3');

INSERT INTO Taken VALUES('2222222222','CCC111','U');
INSERT INTO Taken VALUES('2222222222','CCC222','U');
INSERT INTO Taken VALUES('2222222222','CCC444','U');

INSERT INTO WaitingList VALUES('3333333333','CCC222',1);
INSERT INTO WaitingList VALUES('3333333333','CCC333',1);
INSERT INTO WaitingList VALUES('2222222222','CCC333',2);

INSERT INTO Departments VALUES('Department1', 'D1');
INSERT INTO Departments VALUES('Department2', 'D2');

INSERT INTO DepartmentProgram VALUES('Department1', 'Prog1');
INSERT INTO DepartmentProgram VALUES('Department2', 'Prog2');
INSERT INTO DepartmentProgram VALUES('Department1', 'Prog3'); -- D1 and D2 collaborates on P3
INSERT INTO DepartmentProgram VALUES('Department2', 'Prog3');

INSERT INTO DepartmentCourses VALUES('Department1', 'CCC111');
INSERT INTO DepartmentCourses VALUES('Department2', 'CCC222');
INSERT INTO DepartmentCourses VALUES('Department1', 'CCC333');
INSERT INTO DepartmentCourses VALUES('Department2', 'CCC444');

INSERT INTO Prerequisite VALUES('CCC333', 'CCC444'); -- To read CCC333 you need CCC444

-- new for lab 3
INSERT INTO Registered VALUES ('1111111111', 'CCC666');
INSERT INTO WaitingList VALUES ('2222222222', 'CCC666', 1);
INSERT INTO WaitingList VALUES ('3333333333', 'CCC666', 2);
INSERT INTO WaitingList VALUES ('4444444444', 'CCC666', 3);
INSERT INTO WaitingList VALUES ('5555555555', 'CCC666', 4);

INSERT INTO Registered VALUES ('1111111111', 'CCC777');
INSERT INTO Registered VALUES ('2222222222', 'CCC777');
INSERT INTO WaitingList VALUES ('3333333333', 'CCC777', 1);

-- Triggers 

-- CourseQueuePositions(course,student,place)
CREATE VIEW CourseQueuePositions AS (
    SELECT 
    course,
    student,
    position AS place
    FROM WaitingList
);

--CREATE OR REPLACE VIEW CourseQueuePositions AS (
--  SELECT course, student, ROW_NUMBER() OVER (PARTITION BY course ORDER BY WaitingList.position) AS place
 -- FROM waitinglist
--);

CREATE OR REPLACE FUNCTION register() RETURNS trigger AS $register$
      -- kolla om man få registera sig
            -- du har klarat kriterierna
            -- du är inte redan registerad
        -- kolla om limitedcourse
            -- om ja
                -- kolla om redan är i waitinglist
                    -- om ja
                        -- error
                    -- om nej
                        -- kolla kursen är full
                            -- om ja
                                -- ställ i kö
                            -- om nej
                                -- registera
            -- om nej
                -- registera
    
    DECLARE 
        currentstatus TEXT;
        size INT; -- size of the course
        count INT; -- number of registrated students in the course
        place_in_queue INT;
    BEGIN

    currentstatus := (SELECT status FROM Registrations WHERE student = NEW.student AND course = NEW.course);
    size := (SELECT capacity FROM LimitedCourses WHERE LimitedCourses.code = NEW.course);
    count := (SELECT COUNT(*) FROM Registrations WHERE course = NEW.course AND status = 'registered');
    place_in_queue := (SELECT COUNT(*) FROM Registrations WHERE course = NEW.course AND status = 'waiting');

    -- Om inte registrerad 
    IF NEW.status != 'registered' THEN
        RETURN NEW;
    END IF;

    --Klarat alla kurser innan 
    IF (SELECT COUNT(*) 
        FROM Prerequisite
        LEFT JOIN PassedCourses ON PassedCourses.student = NEW.student AND PassedCourses.course = prerequisite
        WHERE Prerequisite.course = NEW.course AND student IS NULL
        ) > 0 THEN
        RAISE EXCEPTION 'has not passed prerequisite courses';
    END IF;

    --Kolla om du redan klarat kursen
    IF (SELECT grade FROM FinishedCourses WHERE student = NEW.student AND course = NEW.course) != 'U' THEN
        RAISE EXCEPTION 'already passed this course';
    END IF;

    -- Kolla om du redan är registrerad på kursen 
    IF currentstatus = 'registered' THEN
        RAISE EXCEPTION 'already registered on this course';
    END IF;

    --Kolla om redan i waitinglist
    IF currentstatus = 'waiting' THEN
        RAISE EXCEPTION 'already in the waitinglist for this course';
    END IF;


    IF size IS NOT NULL AND count >= size THEN -- the course is full
        INSERT INTO WaitingList VALUES (NEW.student, NEW.course, place_in_queue + 1); -- gets last place in queue
    ELSE
        INSERT INTO Registered VALUES (NEW.student, NEW.course); -- registered to course
    END IF;


    RETURN NEW;
    END;

$register$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION unregister() RETURNS trigger AS $unregister$
     DECLARE
        count INTEGER;
        size INTEGER;
        firstInQueue CHAR(10);
        position_in_queue INTEGER;
        
    BEGIN
        -- If course is not limited we can just remove the student
        IF (OLD.course NOT IN (SELECT code FROM LimitedCourses)) THEN
            DELETE FROM Registered 
            WHERE OLD.student = Registered.student 
            AND OLD.course = Registered.course;
            RETURN OLD;
        END IF;

        count := (SELECT COUNT(*) FROM Registrations WHERE course = OLD.course AND status = 'registered');

        size := (SELECT capacity FROM LimitedCourses WHERE LimitedCourses.code = OLD.course); -- null if not limited course
    
        position_in_queue := (SELECT position FROM WaitingList WHERE student = OLD.student AND course = OLD.course); -- the student who is leaving course/queue

        -- Remove from waiting
        IF (OLD.status = 'waiting') THEN
            DELETE FROM WaitingList WHERE OLD.student = WaitingList.student AND OLD.course = WaitingList.course;
            UPDATE CourseQueuePositions SET place = place - 1 WHERE OLD.course = CourseQueuePositions.course 
            AND CourseQueuePositions.place > position_in_queue;
            RETURN OLD;
        END IF;

        
        -- Only delete from registered if the course is overfull (size < count)
        IF (size < count) THEN
            DELETE FROM Registered 
            WHERE OLD.student = Registered.student 
            AND OLD.course = Registered.course;
            RETURN OLD;
        END IF;

        firstInQueue := (SELECT student FROM CourseQueuePositions WHERE place = 1 AND course = OLD.course);
       
        -- New positions
        IF (firstInQueue != '') THEN
            DELETE FROM WaitingList where student=firstInQueue and course=OLD.course;
            DELETE FROM Registered WHERE student = OLD.student AND course = OLD.course;
            UPDATE WaitingList SET position = position - 1 WHERE
            OLD.course = WaitingList.course;

            INSERT INTO Registered VALUES (firstInQueue, OLD.course);
        
            RAISE NOTICE 'Student removed from course, new student added from queue';
            RETURN OLD;
        END IF;

        DELETE FROM Registered WHERE student = OLD.student AND course = OLD.course;
        RETURN OLD;
    END;
    

    -- If the course is limited and if someone unregistered from the waitinglist
    --IF queue_size_after IS NOT NULL AND queue_size_before IS NOT NULL THEN  -- If there still is a queue

    --   IF queue_size_before > queue_size_after THEN
     --       UPDATE CourseQueuePositions SET place = place - 1
     --       WHERE OLD.course = CourseQueuePositions.course AND CourseQueuePositions.place > position_in_queue;
     --   END IF;

   -- END IF;
$unregister$ LANGUAGE plpgsql;



CREATE TRIGGER register INSTEAD OF INSERT OR UPDATE ON Registrations 
    FOR EACH ROW EXECUTE FUNCTION register();

CREATE TRIGGER unregister INSTEAD OF DELETE ON Registrations 
    FOR EACH ROW EXECUTE FUNCTION unregister();