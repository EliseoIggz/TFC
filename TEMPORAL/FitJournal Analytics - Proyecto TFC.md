**FitJournal Analytics - Sistema Inteligente de Diario Deportivo y Nutricional**

🎯 **Descripción del Proyecto**

Un sistema completo que combina el registro de actividades deportivas y alimentación con análisis estadístico avanzado, machine learning y visualizaciones interactivas para predecir mejoras en la salud y optimizar rutinas personales.

🚀 **Características Principales**

1. **Sistema de Registro Manual Inteligente**
- **Diario deportivo**: Formularios intuitivos para ejercicios, duración, intensidad, sensaciones
- **Diario nutricional**: Base de datos de alimentos local, calculadora de macronutrientes
- **Interfaz adaptativa**: Formularios que se adaptan según el tipo de actividad/comida
- **Análisis de patrones**: El sistema aprende de tus entradas para sugerir valores comunes
2. **Análisis Estadístico y Predictivo**
- **Modelos ML**: Predicción de pérdida de peso, ganancia muscular, resistencia
- **Correlaciones**: Relación entre dieta, ejercicio y métricas de salud
- **Tendencias temporales**: Análisis de progreso a corto y largo plazo
- **Recomendaciones personalizadas**: IA que sugiere mejoras basadas en patrones
3. **Visualizaciones Interactivas**
- **Dashboards dinámicos**: Gráficos en tiempo real con Plotly/Dash
- **Mapas de calor**: Distribución de entrenamientos y patrones alimentarios
- **Análisis comparativo**: Benchmarking personal vs. objetivos
- **Reportes automáticos**: PDFs con resúmenes semanales/mensuales

📚 **Librerías y Tecnologías Innovadoras**

**Core del Sistema**

![](Aspose.Words.53b3d79d-c53d-4201-8685-e5eeb52fa070.001.png)

*## PPrroocceessaammiieennttoo ddee ddaattooss yy aannáálliissiiss![](Aspose.Words.53b3d79d-c53d-4201-8685-e5eeb52fa070.002.png)*

iimmppoorrtt ppaannddaass aass ppdd

iimmppoorrtt nnuummppyy aass nnpp

ffrroomm sskklleeaarrnn..eennsseemmbbllee iimmppoorrtt RRaannddoommFFoorreessttRReeggrreessssoorr,, GGrraaddiieennttBBoooossttiinnggRReeggrreessssoorr ffrroomm sskklleeaarrnn..cclluusstteerr iimmppoorrtt KKMMeeaannss

ffrroomm sskklleeaarrnn..pprreepprroocceessssiinngg iimmppoorrtt SSttaannddaarrddSSccaalleerr

ffrroomm sscciippyy iimmppoorrtt ssttaattss

iimmppoorrtt jjoobblliibb

*## VViissuuaalliizzaacciióónn aavvaannzzaaddaa*

iimmppoorrtt pplloottllyy..ggrraapphh\_\_oobbjjeeccttss aass ggoo

iimmppoorrtt pplloottllyy..eexxpprreessss aass ppxx

ffrroomm pplloottllyy..ssuubbpplloottss iimmppoorrtt mmaakkee\_\_ssuubbpplloottss iimmppoorrtt sseeaabboorrnn aass ssnnss

iimmppoorrtt mmaattpplloottlliibb..ppyypplloott aass pplltt

*## WWeebb ffrraammeewwoorrkk yy ddaasshhbbooaarrdd*

iimmppoorrtt ssttrreeaammlliitt aass sstt

iimmppoorrtt ddaasshh

ffrroomm ddaasshh iimmppoorrtt ddcccc,, hhttmmll,, IInnppuutt,, OOuuttppuutt

**Características Avanzadas**

python![](Aspose.Words.53b3d79d-c53d-4201-8685-e5eeb52fa070.003.png)

*## AAnnáálliissiiss nnuuttrriicciioonnaall yy ddeeppoorrttiivvoo*

ffrroomm nnuuttrriittiioonn\_\_ddaattaa iimmppoorrtt SSppaanniisshhFFooooddDDaattaabbaassee *## BBaassee ddee ddaattooss eessppaaññoollaa* iimmppoorrtt eexxeerrcciissee\_\_ddaattaabbaassee *## BBaassee ddee ddaattooss ddee eejjeerrcciicciiooss MMEETT*

*## BBaassee ddee ddaattooss yy aallmmaacceennaammiieennttoo* iimmppoorrtt ssqqlliittee33

ffrroomm ssqqllaallcchheemmyy iimmppoorrtt ccrreeaattee\_\_eennggiinnee iimmppoorrtt ppiicckkllee

*## AAnnáálliissiiss tteemmppoorraall yy sseerriieess*

ffrroomm ssttaattssmmooddeellss..ttssaa..aarriimmaa..mmooddeell iimmppoorrtt AARRIIMMAA

ffrroomm ssttaattssmmooddeellss..ttssaa..sseeaassoonnaall iimmppoorrtt sseeaassoonnaall\_\_ddeeccoommppoossee ffrroomm pprroopphheett iimmppoorrtt PPrroopphheett *## PPaarraa pprreeddiicccciioonneess tteemmppoorraalleess*

*## AAnnáálliissiiss eessttaaddííssttiiccoo aavvaannzzaaddoo*

ffrroomm sscciippyy..ooppttiimmiizzee iimmppoorrtt mmiinniimmiizzee

ffrroomm sskklleeaarrnn..mmeettrriiccss iimmppoorrtt mmeeaann\_\_aabbssoolluuttee\_\_eerrrroorr,, rr22\_\_ssccoorree

**Librerías Únicas y Originales**

![](Aspose.Words.53b3d79d-c53d-4201-8685-e5eeb52fa070.004.png)

*## AAnnáálliissiiss bbiioommééddiiccoo yy nnuuttrriicciioonnaall![](Aspose.Words.53b3d79d-c53d-4201-8685-e5eeb52fa070.005.png)*

ffrroomm nnuuttrriittiioonn\_\_aannaallyyssiiss iimmppoorrtt MMaaccrrooCCaallccuullaattoorr,, MMiiccrroonnuuttrriieennttTTrraacckkeerr ffrroomm eexxeerrcciissee\_\_sscciieennccee iimmppoorrtt MMEETTCCaallccuullaattoorr,, CCaalloorriieeEEssttiimmaattoorr

ffrroomm hheeaalltthh\_\_mmeettrriiccss iimmppoorrtt BBMMRRCCaallccuullaattoorr,, BBooddyyCCoommppoossiittiioonnEEssttiimmaattoorr

*## PPrroocceessaammiieennttoo ddee lleenngguuaajjee nnaattuurraall ppaarraa aannáálliissiiss ddee tteexxttooss* iimmppoorrtt ssppaaccyy

ffrroomm tteexxttbblloobb iimmppoorrtt TTeexxttBBlloobb

iimmppoorrtt nnllttkk

*## AAnnáálliissiiss ddee ppaattrroonneess tteemmppoorraalleess*

iimmppoorrtt hhoolliiddaayyss *## PPaarraa ccoonnssiiddeerraarr ddííaass ffeessttiivvooss eenn aannáálliissiiss* ffrroomm ddaatteettiimmee iimmppoorrtt ddaatteettiimmee,, ttiimmeeddeellttaa

iimmppoorrtt ccaalleennddaarr

*## BBaasseess ddee ddaattooss nnuuttrriicciioonnaalleess llooccaalleess*

ffrroomm ffoooodd\_\_ccoommppoossiittiioonn\_\_ssppaaiinn iimmppoorrtt BBEEDDCCAA\_\_DDaattaabbaassee *## BBaassee eessppaaññoollaa ooffiicciiaall* iimmppoorrtt nnuuttrriieenntt\_\_rreeqquuiirreemmeennttss *## RReeqquueerriimmiieennttooss nnuuttrriicciioonnaalleess ppoorr ddeemmooggrraaffííaa*

🏗 **Arquitectura del Sistema**

1. **Módulo de Captura de Datos**
- **SmartForms**: Formularios inteligentes que se adaptan al contexto
- **FoodDatabase**: Base de datos nutricional española integrada
- **ActivityTracker**: Sistema de seguimiento manual con autocompletado
- **DataValidation**: Validación inteligente y detección de inconsistencias
2. **Motor de Análisis**
- **HealthMetricsEngine**: Cálculo de métricas de salud (BMI, BFP, VO2 max estimado)
- **CorrelationAnalyzer**: Análisis de correlaciones entre variables
- **PredictiveModels**: Modelos ML para predicciones de progreso
- **PatternRecognition**: Identificación de patrones y anomalías
3. **Sistema de Recomendaciones**
- **NutritionOptimizer**: Optimización de dietas basada en objetivos
- **WorkoutPlanner**: Planificación inteligente de entrenamientos
- **ProgressTracker**: Seguimiento y ajuste de objetivos
- **HealthAlerts**: Alertas proactivas sobre salud
4. **Interfaz y Visualización**
- **InteractiveDashboard**: Dashboard principal con Streamlit/Dash
- **ReportGenerator**: Generación automática de reportes
- **DataExporter**: Exportación a diferentes formatos
- **MobileView**: Versión optimizada para móviles

📊 **Características Técnicas Innovadoras**

1. **Análisis Predictivo Avanzado**

python![](Aspose.Words.53b3d79d-c53d-4201-8685-e5eeb52fa070.006.png)

ccllaassss HHeeaalltthhPPrreeddiiccttoorr::

ddeeff pprreeddiicctt\_\_wweeiigghhtt\_\_lloossss((sseellff,, ccuurrrreenntt\_\_ddaattaa,, ttaarrggeett\_\_ddaattee))::

*## MMooddeelloo qquuee ccoonnssiiddeerraa mmeettaabboolliissmmoo bbaassaall,, eejjeerrcciicciioo,, ddiieettaa* ppaassss

ddeeff eessttiimmaattee\_\_ppeerrffoorrmmaannccee\_\_iimmpprroovveemmeenntt((sseellff,, eexxeerrcciissee\_\_hhiissttoorryy))::

*## PPrreeddiicccciióónn ddee mmeejjoorraass eenn rreennddiimmiieennttoo ddeeppoorrttiivvoo*

ppaassss

ddeeff nnuuttrriittiioonn\_\_iimmppaacctt\_\_aannaallyyssiiss((sseellff,, mmeeaall\_\_ppllaannss))::

*## AAnnáálliissiiss ddeell iimmppaaccttoo nnuuttrriicciioonnaall eenn llaa ssaalluudd* ppaassss

2. **Procesamiento de Imágenes Inteligente**

python![](Aspose.Words.53b3d79d-c53d-4201-8685-e5eeb52fa070.007.png)

ccllaassss FFooooddRReeccooggnniittiioonn::

ddeeff iiddeennttiiffyy\_\_ffoooodd((sseellff,, iimmaaggee))::

*## IIddeennttiiffiiccaacciióónn aauuttoommááttiiccaa ddee aalliimmeennttooss* ppaassss

ddeeff eessttiimmaattee\_\_ppoorrttiioonnss((sseellff,, iimmaaggee,, rreeffeerreennccee\_\_oobbjjeecctt))::

*## EEssttiimmaacciióónn ddee ppoorrcciioonneess uussaannddoo rreeffeerreenncciiaass* ppaassss

ddeeff nnuuttrriittiioonn\_\_eexxttrraaccttiioonn((sseellff,, iiddeennttiiffiieedd\_\_ffooooddss))::

*## EExxttrraacccciióónn aauuttoommááttiiccaa ddee iinnffoorrmmaacciióónn nnuuttrriicciioonnaall* ppaassss

3. **Análisis de Señales Biológicas**

![](Aspose.Words.53b3d79d-c53d-4201-8685-e5eeb52fa070.008.png)

ccllaassss BBiioommeettrriiccAAnnaallyyzzeerr::![](Aspose.Words.53b3d79d-c53d-4201-8685-e5eeb52fa070.009.png)

ddeeff hheeaarrtt\_\_rraattee\_\_vvaarriiaabbiilliittyy((sseellff,, hhrr\_\_ddaattaa))::

*## AAnnáálliissiiss ddee vvaarriiaabbiilliiddaadd ddee ffrreeccuueenncciiaa ccaarrddííaaccaa* ppaassss

ddeeff sslleeeepp\_\_qquuaalliittyy\_\_aasssseessssmmeenntt((sseellff,, sslleeeepp\_\_ddaattaa))::

*## EEvvaalluuaacciióónn ddee ccaalliiddaadd ddeell ssuueeññoo*

ppaassss

ddeeff ssttrreessss\_\_lleevveell\_\_ddeetteeccttiioonn((sseellff,, bbiioommeettrriicc\_\_ddaattaa))::

*## DDeetteecccciióónn ddee nniivveelleess ddee eessttrrééss*

ppaassss

🎨 **Funcionalidades Destacadas**

1. Registro Manual Inteligente
- Formularios que aprenden de tus patrones de entrada
- Autocompletado contextual basado en historial personal
- Detección automática de inconsistencias en datos
2. Base de Datos Nutricional Española Integrada
- Integración completa con BEDCA (Base oficial española)
- Búsqueda inteligente por ingredientes y platos regionales
- Cálculo automático de macros/micros por porción personalizada
3. Formularios Adaptativos Inteligentes
- Formularios que "aprenden" de tus patrones de entrada
- Autocompletado basado en historial personal
- Validación en tiempo real de datos inconsistentes
4. Sistema de Objetivos Dinámicos
- Establecimiento de metas SMART personalizadas
- Ajuste automático de objetivos basado en progreso
- Alertas cuando te desvías de tu plan
5. Análisis Comparativo Temporal
- Comparación con períodos anteriores (mismo mes del año pasado)
- Análisis de estacionalidad en hábitos
- Identificación de patrones cíclicos personales

📈 **Métricas y KPIs del Sistema**

**Salud Física**

- Composición corporal (peso, grasa, músculo)
- Capacidad cardiovascular (VO2 max, frecuencia cardíaca en reposo)
- Fuerza y resistencia (1RM estimado, tiempo de fatiga)
- Flexibilidad y movilidad

**Salud Nutricional**

- Balance calórico
- Distribución de macronutrientes
- Micronutrientes esenciales
- Índice de inflamación dietética

**Bienestar General**

- Calidad del sueño
- Niveles de estrés
- Estado de ánimo (mediante cuestionarios)
- Energía percibida

🔧 **Implementación Técnica**

**Base de Datos**

sql![](Aspose.Words.53b3d79d-c53d-4201-8685-e5eeb52fa070.010.png)

*---- EEssttrruuccttuurraa pprriinncciippaall ddee ttaabbllaass*

CCRREEAATTEE TTAABBLLEE uusseerrss ((iidd,, nnaammee,, bbiirrtthh\_\_ddaattee,, ggeennddeerr,, hheeiigghhtt,, ggooaallss));;

CCRREEAATTEE TTAABBLLEE wwoorrkkoouuttss ((iidd,, uusseerr\_\_iidd,, ddaattee,, ttyyppee,, dduurraattiioonn,, iinntteennssiittyy,, ccaalloorriieess));; CCRREEAATTEE TTAABBLLEE nnuuttrriittiioonn ((iidd,, uusseerr\_\_iidd,, ddaattee,, mmeeaall\_\_ttyyppee,, ffoooodd\_\_iitteemmss,, ccaalloorriieess,, mmaaccrrooss));; CCRREEAATTEE TTAABBLLEE bbiioommeettrriiccss ((iidd,, uusseerr\_\_iidd,, ddaattee,, wweeiigghhtt,, bbooddyy\_\_ffaatt,, hheeaarrtt\_\_rraattee));;

CCRREEAATTEE TTAABBLLEE pprreeddiiccttiioonnss ((iidd,, uusseerr\_\_iidd,, ddaattee,, mmeettrriicc,, pprreeddiicctteedd\_\_vvaalluuee,, ccoonnffiiddeennccee));;

**API Design**

![](Aspose.Words.53b3d79d-c53d-4201-8685-e5eeb52fa070.011.png)

*## RREESSTTffuull AAPPII eennddppooiinnttss ![](Aspose.Words.53b3d79d-c53d-4201-8685-e5eeb52fa070.012.png)*//aappii//vv11//uusseerrss//{{uusseerr\_\_iidd}}//wwoorrkkoouuttss //aappii//vv11//uusseerrss//{{uusseerr\_\_iidd}}//nnuuttrriittiioonn //aappii//vv11//uusseerrss//{{uusseerr\_\_iidd}}//pprreeddiiccttiioonnss //aappii//vv11//uusseerrss//{{uusseerr\_\_iidd}}//rreeppoorrttss //aappii//vv11//ffoooodd//rreeccooggnniizzee ((PPOOSSTT ccoonn iimmaaggeenn)) //aappii//vv11//vvooiiccee//pprroocceessss ((PPOOSSTT ccoonn aauuddiioo))

**Deployment**

- **Backend**: FastAPI + PostgreSQL + Redis
- **Frontend**: Streamlit/Dash para prototipo, React para versión final
- **ML Pipeline**: MLflow para versionado de modelos
- **Containerización**: Docker + Docker Compose
- **Cloud**: AWS/GCP con auto-scaling

🎯 **Entregables del TFC**

1. **Aplicación Funcional** - Sistema completo desplegado
1. **Modelos ML Entrenados** - Algoritmos de predicción validados
1. **Dashboard Interactivo** - Visualizaciones en tiempo real
1. **Documentación Técnica** - Arquitectura y APIs documentadas
1. **Dataset Sintético** - Datos de prueba para demostración
1. **Análisis de Resultados** - Validación estadística de predicciones
1. **Manual de Usuario** - Guía completa de uso
1. **Video Demo** - Demostración de todas las funcionalidades

💡 **Valor Diferencial**

- **Enfoque Holístico**: Combina deporte, nutrición y bienestar
- **IA Personalizada**: Modelos adaptados a cada usuario
- **Tecnología Cutting-edge**: Uso de librerías especializadas poco comunes
- **Aplicabilidad Real**: Solución práctica para un problema cotidiano
- **Escalabilidad**: Arquitectura preparada para crecimiento
- **Innovación**: Características únicas como análisis por voz e imagen

Este proyecto demuestra dominio técnico avanzado, aplicación práctica de ML/IA, y capacidad de integrar múltiples tecnologías en una solución coherente y útil.
