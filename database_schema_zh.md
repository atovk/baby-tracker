# SQLite 数据库模式文档

本文档概述了 `EasyLog.db` SQLite 数据库的模式，包括表结构、列描述和推断的关系。

## 核心表

### `Baby` (婴儿表)

存储每个婴儿的信息。

- `ID` (TEXT, 主键): 婴儿的唯一标识符。
- `Timestamp` (REAL): 记录创建或最后更新的时间戳。
- `Name` (TEXT): 婴儿的名字。
- `DOB` (REAL): 婴儿的出生日期 (Unix 时间戳)。
- `DueDay` (TEXT): 婴儿的预产期 (当前为 `None`)。
- `Gender` (INTEGER): 婴儿的性别 (例如，0 代表女性，1 代表男性)。
- `Picture` (TEXT): 婴儿图片的 文件名或路径 (当前为 `None`)。

## 活动记录表

这些表记录了与婴儿相关的各种活动。大多数包含：

- `ID` (TEXT, 主键): 日志条目的唯一标识符。
- `Timestamp` (REAL): 日志条目创建时的时间戳。
- `Time` (REAL): 活动的具体时间 (Unix 时间戳)。
- `Note` (TEXT): 用户提供的活动备注。
- `HasPicture` (INTEGER):布尔值 (0 或 1)，指示此活动是否关联了图片。
- `BabyID` (TEXT, 外键): 引用 `Baby.ID`。标识此活动所属的婴儿。

### `Nursing` (哺乳表)

记录哺乳过程。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `DescID` (TEXT, 外键 -> `FeedDesc.ID`, 可能用于记录类型如“母乳”): 哺乳的描述或类型 (当前为 `None`)。
- `FinishSide` (INTEGER): 喂养结束时在哪一侧 (例如，0 代表左侧，1 代表右侧，2 代表两侧/未知)。
- `LeftDuration` (INTEGER): 左侧喂养的持续时间 (秒或分钟)。
- `RightDuration` (INTEGER): 右侧喂养的持续时间。
- `BothDuration` (INTEGER): 如果在两侧喂养的持续时间 (如果 `FinishSide` 指示“两侧”，则可能是总时间或特定时间)。

### `Formula` (配方奶表)

记录配方奶喂养过程。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `DescID` (TEXT, 外键 -> `FeedDesc.ID`, 可能用于记录类型如“配方奶”): 配方奶的描述或类型 (当前为 `None`)。
- `Amount` (REAL): 消耗的配方奶量。
- `IsEnglishScale` (INTEGER): 布尔值 (0 或 1)，指示量是否以英制单位 (例如盎司) 而不是公制单位 (例如毫升) 表示。

### `Pump` (吸奶表)

记录吸奶过程。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `FinishSide` (INTEGER): 吸奶结束时在哪一侧。
- `Sides` (INTEGER): 吸奶的侧面 (例如，左侧，右侧，两侧)。
- `Amount` (REAL): 总吸奶量。
- `IsEnglishScale` (INTEGER): 量的单位制。
- `Label` (TEXT): 用户定义的吸出奶的标签。
- `PumpedID` (TEXT): 如果这是摘要记录，则可能链接到 `Pumped.ID`。
- `LeftAmount` (REAL): 从左侧吸出的量。
- `RightAmount` (REAL): 从右侧吸出的量。
- `LeftDuration` (INTEGER): 左侧吸奶的持续时间。
- `RightDuration` (INTEGER): 右侧吸奶的持续时间。

### `Pumped` (已吸出母乳表)

记录已吸出母乳的详细信息 (可能用于稍后喂养)。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `DescID` (TEXT): 描述 ID，可能链接到通用描述表或类型。
- `Amount` (REAL): 吸出母乳的量。
- `IsEnglishScale` (INTEGER): 量的单位制。
- `PumpID` (TEXT, 外键 -> `Pump.ID`): 链接到吸奶过程。

### `OtherFeed` (其他喂养表)

记录其他类型的喂养 (例如固体食物)。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `DescID` (TEXT, 外键 -> `OtherFeedSelection.ID`): 描述其他喂养的类型。
- `TypeID` (TEXT): 可能的另一种喂养类型分类。
- `Amount` (REAL): 消耗量。
- `IsEnglishScale` (INTEGER): 量的单位制。
- `Unit` (TEXT): 计量单位 (例如克，盎司)。

### `Diaper` (尿布表)

记录换尿布的情况。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `Status` (INTEGER): 尿布状态 (例如，湿，脏，混合)。
- `PeeColor` (INTEGER): 尿液颜色。
- `PooColor` (INTEGER): 粪便颜色。
- `Amount` (INTEGER): 尿布中的量 (例如，少量，中量，大量)。
- `Texture` (INTEGER): 粪便质地。
- `Flag` (INTEGER): 任何特殊标记或指示符。

### `Sleep` (睡眠表)

记录睡眠过程。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `Duration` (INTEGER): 睡眠持续时间 (秒或分钟)。
- `LocationID` (TEXT, 外键 -> `SleepLocationSelection.ID`): 婴儿睡觉的地方。
- `DescID` (TEXT, 外键 -> `SleepDesc.ID`): 婴儿如何入睡的描述。

### `Bath` (洗澡表)

记录洗澡时间。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `DescID` (TEXT, 外键 -> `BathDesc.ID`): 洗澡类型。

### `OtherActivity` (其他活动表)

记录其他杂项活动。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `DescID` (TEXT, 外键 -> `OtherActivityDesc.ID`): 活动类型。
- `LocationID` (TEXT, 外键 -> `OtherActivityLocationSelection.ID`): 活动地点。
- `Duration` (INTEGER): 活动持续时间。

### `Milestone` (里程碑表)

记录婴儿达成的发育里程碑。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `MilestoneSelectionID` (TEXT, 外键 -> `MilestoneSelection.ID`): 达成的具体里程碑。

### `Temperature` (体温表)

记录婴儿的体温读数。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `Temp` (REAL): 体温读数。
- `IsEnglishScale` (INTEGER): 体温单位制 (华氏度 vs 摄氏度)。

### `Growth` (生长表)

记录生长测量值 (体重，身长，头围)。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `Weight` (REAL): 婴儿体重。
- `Length` (REAL): 婴儿身长/身高。
- `Head` (REAL): 婴儿头围。
- `IsEnglishLengthScale` (INTEGER): 长度单位制。
- `IsEnglishWeightScale` (INTEGER): 重量单位制。

### `Sick` (生病表)

记录生病或症状的情况。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `Symptom` (TEXT, 外键 -> `SickDesc.ID`): 症状描述。

### `Medicine` (药物表)

记录用药情况。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `MedID` (TEXT, 外键 -> `MedicineSelection.ID`): 服用的药物。
- `Amount` (REAL): 服用药物的量。

### `Vaccine` (疫苗表)

记录疫苗接种情况。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `VaccID` (TEXT, 外键 -> `VaccineSelection.ID`): 接种的疫苗。
- `DocVisitID` (TEXT, 外键 -> `DoctorVisit.ID`): 链接到接种疫苗的医生就诊记录。

### `Allergen` (过敏原表)

记录过敏反应。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `SourceID` (TEXT, 外键 -> `AllergenSourceSelection.ID`): 过敏原来源。
- `Reaction` (TEXT): 过敏反应描述。
- `Severity` (INTEGER): 反应严重程度。
- `NotSure` (INTEGER): 布尔值，指示对过敏原/反应不确定。

### `DoctorVisit` (就医表)

记录就医情况。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `IsAppointment` (INTEGER): 布尔值，是否为预约就诊。
- `VisitType` (TEXT): 就医类型。
- `DoctorID` (TEXT, 外键 -> `DoctorSelection.ID`): 就诊的医生。
- `DoctorNote` (TEXT): 医生的备注。
- `Symptom` (TEXT): 讨论或观察到的症状。
- `GrowthID` (TEXT, 外键 -> `Growth.ID`): 链接到就诊期间记录的生长数据。
- `SickID` (TEXT, 外键 -> `Sick.ID`): 链接到与就诊相关的生病记录。

### `DoctorVisitMedicine` (就医药方表)

链接在医生就诊期间开具或讨论的药物。(关联表)

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `DoctorVisitID` (TEXT, 外键 -> `DoctorVisit.ID`)
- `MedID` (TEXT, 外键 -> `MedicineSelection.ID`)

### `HealthQuestion` (健康问题表)

记录健康相关问题和答案，可能来自医生就诊。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `Question` (TEXT): 提出的健康问题。
- `Answer` (TEXT): 收到的答案。
- `DoctorVisitID` (TEXT, 外键 -> `DoctorVisit.ID`): 链接到相关的医生就诊记录。

### `Joy` (快乐时刻表)

记录快乐时刻或积极事件。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)

### `Journal` (日记表)

通用日记条目。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `Time` (REAL)
- `Note` (TEXT)
- `HasPicture` (INTEGER)
- `BabyID` (TEXT, 外键 -> `Baby.ID`)

## 选择/描述表 (查找表)

这些表为各种活动提供预定义选项或描述。
通用列:

- `ID` (TEXT, 主键): 选择项的唯一标识符。
- `Timestamp` (REAL): 创建/更新的时间戳。
- `Name` (TEXT): 项目的显示名称。
- `Description` (TEXT): 项目的详细描述。

### `SickDesc` (疾病描述表)

预定义的疾病症状描述。

- `ID`, `Timestamp`, `Name`, `Description`

### `BathDesc` (洗澡描述表)

预定义的洗澡类型描述。

- `ID`, `Timestamp`, `Name`, `Description`

### `SleepDesc` (睡眠描述表)

预定义的婴儿如何入睡的描述。

- `ID`, `Timestamp`, `Name`, `Description`

### `FeedDesc` (喂养描述表)

与喂养相关的预定义描述 (例如，吐奶，打嗝)。

- `ID`, `Timestamp`, `Name`, `Description`

### `OtherActivityDesc` (其他活动描述表)

其他活动的预定义描述。

- `ID`, `Timestamp`, `Name`, `Description`

### `MilestoneSelection` (里程碑选择表)

预定义的发育里程碑。

- `ID`, `Timestamp`, `Name`, `Description`
- `ForAge` (INTEGER): 此里程碑的典型年龄 (月或代码)。
- `BabyID` (TEXT): (此处不寻常，通常选择表是通用的。可能用于每个婴儿的自定义里程碑，但示例显示为 `None`)。

### `DoctorSelection` (医生选择表)

医生信息。

- `ID`, `Timestamp`, `Name`, `Description`
- `Address` (TEXT): 医生地址。
- `ClinicName` (TEXT): 诊所名称。
- `PhoneNumber` (TEXT): 医生电话号码。

### `MedicineSelection` (药物选择表)

预定义药物的信息。

- `ID`, `Timestamp`, `Name`, `Description`
- `IsPrescription` (INTEGER): 布尔值，是否为处方药。
- `AmountPerTime` (REAL): 标准剂量。
- `Unit` (TEXT): `AmountPerTime` 的单位。
- `Interval` (INTEGER): 标准给药间隔 (例如，小时或分钟)。

### `VaccineSelection` (疫苗选择表)

预定义疫苗的信息。

- `ID`, `Timestamp`, `Name`, `Description`
- `ForAge` (INTEGER): 此疫苗的典型年龄 (月或代码)。

### `OtherFeedSelection` (其他喂养选择表)

其他喂养类型 (固体食物等) 的预定义。

- `ID`, `Timestamp`, `Name`, `Description`
- `IsBottle` (INTEGER): 布尔值，此喂养类型是否通常用奶瓶喂养。

### `AllergenSourceSelection` (过敏原来源选择表)

预定义的过敏原来源。

- `ID`, `Timestamp`, `Name`, `Description`

### `SleepLocationSelection` (睡眠地点选择表)

婴儿可能睡觉的预定义地点。

- `ID`, `Timestamp`, `Name`, `Description`

### `OtherActivityLocationSelection` (其他活动地点选择表)

其他活动的预定义地点。

- `ID`, `Timestamp`, `Name`, `Description`

## 媒体和系统表

### `Picture` (图片表)

存储链接到活动的图片信息。

- `ID` (TEXT, 主键)
- `Timestamp` (REAL)
- `ActivityID` (TEXT, 外键): 链接到活动表中条目的 `ID` (例如 `Nursing.ID`, `Sleep.ID`)。具体表需要推断或存储在其他地方。
- `Type` (TEXT): 图片类型或上下文。
- `FileName` (TEXT): 图片文件名。
- `Thumbnail` (TEXT): 图片缩略图文件名。

### `PhotoList` (照片列表)

可能是照片文件名的列表。

- `PhotoFile` (TEXT)

### `PhotoDownloadList` (照片下载列表)

跟踪照片的下载情况。

- `PhotoFile` (TEXT)
- `DownloadCount` (INTEGER)

### `TransactionLog` (事务日志表)

记录事务或操作，可能用于同步或撤销。

- `ID` (TEXT, 主键)
- `OpCode` (TEXT): 操作码。
- `Log` (TEXT): 日志消息或数据。

### `sqlite_sequence` (SQLite 序列发生器表)

SQLite 使用的系统表，用于跟踪使用 `AUTOINCREMENT` 的表的自动递增主键。

- `name` (TEXT): 表名。
- `seq` (INTEGER): 该表的最后一个使用的序列号。

### `MergedTransaction` (合并事务表)

可能与数据同步相关。

- `DeviceID` (TEXT)
- `SyncID` (TEXT)

### `ReliveList` (重温列表)

仅从结构上看用途不明，可能与“重温”功能相关。

- `ID` (TEXT)

### `Progress` (进度表)

跟踪各种指标的进度。

- `BabyID` (TEXT, 外键 -> `Baby.ID`)
- `ProgressType` (TEXT): 跟踪的进度类型 (例如，“体重”，“身高”，“喂养量”)。
- `ProgressID` (TEXT): 此进度条目的唯一 ID。
- `ProgressTime` (REAL): 进度数据点的时间戳。
- `ProgressValue` (REAL): 进度指标的值。

### `ProgressPump` (吸奶进度表)

专门跟踪与吸奶相关的进度。

- `ProgressType` (TEXT): 吸奶进度类型。
- `ProgressID` (TEXT): 唯一 ID。
- `ProgressTime` (REAL): 时间戳。
- `ProgressValue` (REAL): 指标的值。

---
*此模式是根据提供的表结构推断出来的。关系基于外键的通用命名约定 (例如 `BabyID`, `DescID`)。实际约束和详细逻辑需要更深入地检查应用程序代码或数据库 DDL。*
