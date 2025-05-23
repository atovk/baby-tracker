# SQLite Database Schema Documentation

This document outlines the schema for the `EasyLog.db` SQLite database, including table structures, column descriptions, and inferred relationships.

## Core Tables

### `Baby`

Stores information about each baby.

- `ID` (TEXT, Primary Key): Unique identifier for the baby.
- `Timestamp` (REAL): Timestamp of when the record was created or last updated.
- `Name` (TEXT): Name of the baby.
- `DOB` (REAL): Date of birth of the baby (Unix timestamp).
- `DueDay` (TEXT): Due date of the baby (currently `None`).
- `Gender` (INTEGER): Gender of the baby (e.g., 0 for female, 1 for male).
- `Picture` (TEXT): Filename or path to the baby's picture (currently `None`).

## Activity Logging Tables

These tables log various activities related to the babies. Most contain:

- `ID` (TEXT, Primary Key): Unique identifier for the log entry.
- `Timestamp` (REAL): Timestamp of when the log entry was created.
- `Time` (REAL): Specific time of the activity (Unix timestamp).
- `Note` (TEXT): User-provided notes for the activity.
- `HasPicture` (INTEGER): Boolean (0 or 1) indicating if a picture is associated with this activity.
- `BabyID` (TEXT, Foreign Key): References `Baby.ID`. Identifies the baby this activity pertains to.

### `Nursing`

Logs nursing sessions.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `DescID` (TEXT, Foreign Key -> `FeedDesc.ID`, possibly for type like 'Breast milk'): Description or type of nursing (currently `None`).
- `FinishSide` (INTEGER): Which side feeding finished on (e.g., 0 for Left, 1 for Right, 2 for Both/Unknown).
- `LeftDuration` (INTEGER): Duration of feeding on the left side (in seconds or minutes).
- `RightDuration` (INTEGER): Duration of feeding on the right side.
- `BothDuration` (INTEGER): Duration if fed on both sides (might be total or specific if `FinishSide` indicates 'Both').

### `Formula`

Logs formula feeding sessions.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `DescID` (TEXT, Foreign Key -> `FeedDesc.ID`, possibly for type like 'Formula'): Description or type of formula (currently `None`).
- `Amount` (REAL): Amount of formula consumed.
- `IsEnglishScale` (INTEGER): Boolean (0 or 1) indicating if the amount is in imperial units (e.g., oz) vs. metric (e.g., ml).

### `Pump`

Logs breast pumping sessions.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `FinishSide` (INTEGER): Which side pumping finished on.
- `Sides` (INTEGER): Sides pumped (e.g., left, right, both).
- `Amount` (REAL): Total amount pumped.
- `IsEnglishScale` (INTEGER): Unit system for amount.
- `Label` (TEXT): User-defined label for the pumped milk.
- `PumpedID` (TEXT): Potentially links to `Pumped.ID` if this is a summary record.
- `LeftAmount` (REAL): Amount pumped from the left side.
- `RightAmount` (REAL): Amount pumped from the right side.
- `LeftDuration` (INTEGER): Duration of pumping on the left side.
- `RightDuration` (INTEGER): Duration of pumping on the right side.

### `Pumped`

Logs details about milk that has been pumped (likely for feeding later).

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `DescID` (TEXT): Description ID, possibly linking to a general description table or type.
- `Amount` (REAL): Amount of pumped milk.
- `IsEnglishScale` (INTEGER): Unit system for amount.
- `PumpID` (TEXT, Foreign Key -> `Pump.ID`): Links to the pumping session.

### `OtherFeed`

Logs other types of feeding (e.g., solids).

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `DescID` (TEXT, Foreign Key -> `OtherFeedSelection.ID`): Describes the type of other feed.
- `TypeID` (TEXT): Potentially another classification for the feed type.
- `Amount` (REAL): Amount consumed.
- `IsEnglishScale` (INTEGER): Unit system for amount.
- `Unit` (TEXT): Unit of measurement (e.g., grams, oz).

### `Diaper`

Logs diaper changes.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `Status` (INTEGER): Diaper status (e.g., wet, dirty, mixed).
- `PeeColor` (INTEGER): Color of urine.
- `PooColor` (INTEGER): Color of stool.
- `Amount` (INTEGER): Amount in diaper (e.g., small, medium, large).
- `Texture` (INTEGER): Texture of stool.
- `Flag` (INTEGER): Any special flag or indicator.

### `Sleep`

Logs sleep sessions.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `Duration` (INTEGER): Duration of sleep (in seconds or minutes).
- `LocationID` (TEXT, Foreign Key -> `SleepLocationSelection.ID`): Where the baby slept.
- `DescID` (TEXT, Foreign Key -> `SleepDesc.ID`): Description of how the baby fell asleep.

### `Bath`

Logs bath times.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `DescID` (TEXT, Foreign Key -> `BathDesc.ID`): Type of bath.

### `OtherActivity`

Logs other miscellaneous activities.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `DescID` (TEXT, Foreign Key -> `OtherActivityDesc.ID`): Type of activity.
- `LocationID` (TEXT, Foreign Key -> `OtherActivityLocationSelection.ID`): Location of the activity.
- `Duration` (INTEGER): Duration of the activity.

### `Milestone`

Logs developmental milestones achieved by the baby.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `MilestoneSelectionID` (TEXT, Foreign Key -> `MilestoneSelection.ID`): The specific milestone achieved.

### `Temperature`

Logs baby's temperature readings.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `Temp` (REAL): Temperature reading.
- `IsEnglishScale` (INTEGER): Unit system for temperature (Fahrenheit vs Celsius).

### `Growth`

Logs growth measurements (weight, length, head circumference).

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `Weight` (REAL): Baby's weight.
- `Length` (REAL): Baby's length/height.
- `Head` (REAL): Baby's head circumference.
- `IsEnglishLengthScale` (INTEGER): Unit system for length.
- `IsEnglishWeightScale` (INTEGER): Unit system for weight.

### `Sick`

Logs instances of sickness or symptoms.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `Symptom` (TEXT, Foreign Key -> `SickDesc.ID`): Description of the symptom.

### `Medicine`

Logs medicine administrations.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `MedID` (TEXT, Foreign Key -> `MedicineSelection.ID`): The medicine administered.
- `Amount` (REAL): Amount of medicine given.

### `Vaccine`

Logs vaccinations.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `VaccID` (TEXT, Foreign Key -> `VaccineSelection.ID`): The vaccine administered.
- `DocVisitID` (TEXT, Foreign Key -> `DoctorVisit.ID`): Links to the doctor visit where the vaccine was given.

### `Allergen`

Logs allergic reactions.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `SourceID` (TEXT, Foreign Key -> `AllergenSourceSelection.ID`): The source of the allergen.
- `Reaction` (TEXT): Description of the allergic reaction.
- `Severity` (INTEGER): Severity of the reaction.
- `NotSure` (INTEGER): Boolean indicating uncertainty about the allergen/reaction.

### `DoctorVisit`

Logs doctor visits.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `IsAppointment` (INTEGER): Boolean, if it was a scheduled appointment.
- `VisitType` (TEXT): Type of doctor visit.
- `DoctorID` (TEXT, Foreign Key -> `DoctorSelection.ID`): The doctor visited.
- `DoctorNote` (TEXT): Notes from the doctor.
- `Symptom` (TEXT): Symptoms discussed or observed.
- `GrowthID` (TEXT, Foreign Key -> `Growth.ID`): Links to a growth record taken during the visit.
- `SickID` (TEXT, Foreign Key -> `Sick.ID`): Links to a sickness record related to the visit.

### `DoctorVisitMedicine`

Links medicines prescribed or discussed during a doctor visit. (Association Table)

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `DoctorVisitID` (TEXT, Foreign Key -> `DoctorVisit.ID`)
- `MedID` (TEXT, Foreign Key -> `MedicineSelection.ID`)

### `HealthQuestion`

Logs health-related questions and answers, possibly from doctor visits.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `Question` (TEXT): The health question asked.
- `Answer` (TEXT): The answer received.
- `DoctorVisitID` (TEXT, Foreign Key -> `DoctorVisit.ID`): Links to the relevant doctor visit.

### `Joy`

Logs moments of joy or positive events.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)

### `Journal`

General journal entries.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)

## Selection/Description Tables (Lookup Tables)

These tables provide predefined options or descriptions for various activities.
Common columns:

- `ID` (TEXT, Primary Key): Unique identifier for the selection item.
- `Timestamp` (REAL): Timestamp of creation/update.
- `Name` (TEXT): Display name of the item.
- `Description` (TEXT): Detailed description of the item.

### `SickDesc`

Predefined descriptions for sickness symptoms.

- `ID`, `Timestamp`, `Name`, `Description`

### `BathDesc`

Predefined descriptions for bath types.

- `ID`, `Timestamp`, `Name`, `Description`

### `SleepDesc`

Predefined descriptions for how a baby fell asleep.

- `ID`, `Timestamp`, `Name`, `Description`

### `FeedDesc`

Predefined descriptions related to feeding (e.g., spit up, burped).

- `ID`, `Timestamp`, `Name`, `Description`

### `OtherActivityDesc`

Predefined descriptions for other activities.

- `ID`, `Timestamp`, `Name`, `Description`

### `MilestoneSelection`

Predefined developmental milestones.

- `ID`, `Timestamp`, `Name`, `Description`
- `ForAge` (INTEGER): Typical age (in months or a code) for this milestone.
- `BabyID` (TEXT): (Unusual here, usually selection tables are generic. Could be for custom milestones per baby, but sample shows `None`).

### `DoctorSelection`

Information about doctors.

- `ID`, `Timestamp`, `Name`, `Description`
- `Address` (TEXT): Doctor's address.
- `ClinicName` (TEXT): Name of the clinic.
- `PhoneNumber` (TEXT): Doctor's phone number.

### `MedicineSelection`

Information about predefined medicines.

- `ID`, `Timestamp`, `Name`, `Description`
- `IsPrescription` (INTEGER): Boolean, if it's a prescription medicine.
- `AmountPerTime` (REAL): Standard dosage amount.
- `Unit` (TEXT): Unit for `AmountPerTime`.
- `Interval` (INTEGER): Standard interval between doses (e.g., in hours or minutes).

### `VaccineSelection`

Information about predefined vaccines.

- `ID`, `Timestamp`, `Name`, `Description`
- `ForAge` (INTEGER): Typical age (in months or a code) for this vaccine.

### `OtherFeedSelection`

Predefined types of other feeds (solids, etc.).

- `ID`, `Timestamp`, `Name`, `Description`
- `IsBottle` (INTEGER): Boolean, if this feed type is typically given in a bottle.

### `AllergenSourceSelection`

Predefined sources of allergens.

- `ID`, `Timestamp`, `Name`, `Description`

### `SleepLocationSelection`

Predefined locations where a baby might sleep.

- `ID`, `Timestamp`, `Name`, `Description`

### `OtherActivityLocationSelection`

Predefined locations for other activities.

- `ID`, `Timestamp`, `Name`, `Description`

## Media and System Tables

### `Picture`

Stores information about pictures linked to activities.

- `ID` (TEXT, Primary Key)
- `Timestamp` (REAL)
- `ActivityID` (TEXT, Foreign Key): Links to the `ID` of an entry in an activity table (e.g., `Nursing.ID`, `Sleep.ID`). The specific table needs to be inferred or stored elsewhere.
- `Type` (TEXT): Type of picture or context.
- `FileName` (TEXT): Name of the image file.
- `Thumbnail` (TEXT): Name of the thumbnail file for the image.

### `PhotoList`

Likely a list of photo file names.

- `PhotoFile` (TEXT)

### `PhotoDownloadList`

Tracks downloads for photos.

- `PhotoFile` (TEXT)
- `DownloadCount` (INTEGER)

### `TransactionLog`

Logs transactions or operations, possibly for sync or undo.

- `ID` (TEXT, Primary Key)
- `OpCode` (TEXT): Operation code.
- `Log` (TEXT): Log message or data.

### `sqlite_sequence`

System table used by SQLite to track auto-incrementing primary keys for tables that use `AUTOINCREMENT`.

- `name` (TEXT): Name of the table.
- `seq` (INTEGER): The last used sequence number for that table.

### `MergedTransaction`

Likely related to data synchronization.

- `DeviceID` (TEXT)
- `SyncID` (TEXT)

### `ReliveList`

Purpose unclear from structure alone, possibly related to a "Relive" feature.

- `ID` (TEXT)

### `Progress`

Tracks progress for various metrics.

- `BabyID` (TEXT, Foreign Key -> `Baby.ID`)
- `ProgressType` (TEXT): Type of progress being tracked (e.g., 'weight', 'height', 'feeding_amount').
- `ProgressID` (TEXT): Unique ID for this progress entry.
- `ProgressTime` (REAL): Timestamp for the progress data point.
- `ProgressValue` (REAL): The value of the progress metric.

### `ProgressPump`

Tracks progress specifically related to pumping.

- `ProgressType` (TEXT): Type of pumping progress.
- `ProgressID` (TEXT): Unique ID.
- `ProgressTime` (REAL): Timestamp.
- `ProgressValue` (REAL): Value of the metric.

---
*This schema is inferred from the provided table structures. Relationships are based on common naming conventions for foreign keys (e.g., `BabyID`, `DescID`). Actual constraints and detailed logic would require deeper inspection of the application code or database DDL.*
