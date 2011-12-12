---
--- Whiteboard SQL schema
--- Developed on PostgreSQL 9.1
---

---
--- Types
---

CREATE TYPE doctype AS ENUM('assignment', 'response', 'document');

---
--- Tables
---

CREATE TABLE Users (
    caseid varchar(6) NOT NULL,

    PRIMARY KEY (caseid)
);

CREATE TABLE LoginLog (
    timestamp timestamp NOT NULL,
    caseid varchar(6) NOT NULL,
    ip_address inet NOT NULL,
    cas_ticket varchar(256) NOT NULL,

    PRIMARY KEY (timestamp, cas_ticket),
    FOREIGN KEY (caseid) REFERENCES Users ON DELETE RESTRICT
);

CREATE TABLE Courses (
    courseid serial NOT NULL,
    code varchar(7) NOT NULL,
    term varchar(10) NOT NULL,
    title varchar(256) NOT NULL,

    PRIMARY KEY (courseid)
);

CREATE TABLE Announcements (
    announcementid serial NOT NULL,
    "date" date NOT NULL,
    content text NOT NULL,
    courseid integer NOT NULL,
    caseid varchar(6) NOT NULL,

    PRIMARY KEY (announcementid),
    FOREIGN KEY (courseid) REFERENCES Courses ON DELETE CASCADE,
    FOREIGN KEY (caseid) REFERENCES Users ON DELETE SET NULL
);


CREATE TABLE Assignments (
    assignmentid serial NOT NULL,
    title varchar(256) NOT NULL,
    due date NOT NULL,
    points integer NOT NULL,
    courseid integer NOT NULL,

    PRIMARY KEY (assignmentid),
    FOREIGN KEY (courseid) REFERENCES Courses ON DELETE CASCADE
);

CREATE TABLE Documents (
    documentid serial NOT NULL,
    isfolder boolean NOT NULL,
    name varchar(256) NOT NULL,
    path varchar(256) NOT NULL,
    courseid integer NOT NULL,
    assignmentid integer,
    parent integer,
    type doctype NOT NULL

    PRIMARY KEY (documentid),
    FOREIGN KEY (courseid) REFERENCES Courses ON DELETE CASCADE,
    FOREIGN KEY (assignmentid) REFERENCES Assignments ON DELETE CASCADE,
    FOREIGN KEY (parent) REFERENCES Documents ON DELETE CASCADE
);

CREATE TABLE Grades (
    assignmentid integer NOT NULL,
    caseid varchar(6) NOT NULL,
    score integer NOT NULL,

    PRIMARY KEY (assignmentid, caseid),
    FOREIGN KEY (assignmentid) REFERENCES Assignments ON DELETE CASCADE,
    FOREIGN KEY (caseid) REFERENCES Users ON DELETE CASCADE
);

CREATE TABLE Roles (
    caseid varchar(6) NOT NULL,
    courseid integer NOT NULL,
    rolename varchar(256) NOT NULL,

    PRIMARY KEY (caseid, courseid, rolename),
    FOREIGN KEY (caseid) REFERENCES Users ON DELETE CASCADE,
    FOREIGN KEY (courseid) REFERENCES Courses ON DELETE CASCADE
);

---
--- Views
---

CREATE VIEW CourseRegistration
AS SELECT C.courseid, C.code, C.term, C.title, R.caseid, R.rolename FROM Courses C, Roles R WHERE C.courseid = R.courseid AND C.courseid > 0;
    
---
--- Procedures
---

CREATE FUNCTION create_default_role() RETURNS trigger LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Roles (caseid, courseid, rolename) VALUES (NEW.caseid, 0, 'student');
    RETURN NULL;
END;
$$;

---
--- Triggers
---

CREATE TRIGGER create_default_role AFTER INSERT ON Users FOR EACH ROW EXECUTE PROCEDURE create_default_role();

---
--- Initial values
---

INSERT INTO Courses VALUES (0, 'root', '', 'Whiteboard Site Course');
