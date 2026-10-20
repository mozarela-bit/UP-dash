# Laboratorio práctico N.° 02 · People Analytics

## 1. Problema y objetivos de negocio

**Problema:** la compañía necesita comprender qué características laborales y de experiencia presentan mayores tasas descriptivas de turnover para priorizar análisis e intervenciones de corto plazo.

**Objetivo general:** desarrollar un dashboard descriptivo que permita monitorear la tasa de turnover y explorar diferencias entre segmentos.

**Objetivos específicos:**
1. Medir el volumen y la tasa global de turnover.
2. Comparar la tasa por función, edad, sobretiempo, viajes y rango salarial.
3. Explorar satisfacción, balance, carrera, antigüedad y compensación.
4. Formular hipótesis verificables con análisis posteriores.
5. Traducir hallazgos descriptivos en prioridades de revisión organizacional.

## 2. Tipos de variables

- **Identificador:** `ID_Empleado`.
- **Objetivo binario:** `TO`, `TO_Decod`.
- **Categóricas nominales:** función, rol, área educativa, género, estado civil, viaje de negocio, sobretiempo.
- **Categóricas ordinales:** grupo de edad, rango salarial, niveles de satisfacción, participación, balance, nivel educativo, nivel de trabajo y rendimiento.
- **Numéricas discretas:** edad, distancia, compañías previas, horas de capacitación, años trabajados, años en compañía, rol, promoción y manager.
- **Numéricas continuas o monetarias:** salarios diario, por hora y mensual; aumento salarial.

## 3. Hallazgos descriptivos de la base completa

La base contiene 1,191 registros, 203 casos de turnover y una tasa global de 17.0%.

- Con sobretiempo: 33.0% de turnover, frente a 10.8% sin sobretiempo.
- Viajes de alta frecuencia: 25.9%, frente a 8.6% sin viajes.
- Grupo de 18 a 25 años: 35.8%; grupo de 26 a 35: 19.1%; grupo de 36 a 45: 9.3%.
- Hasta 5K: 22.3%; más de 15K: 3.9%.
- Balance laboral nivel 1: 37.1%.
- Por función: Recursos Humanos 23.5%, Ventas 20.9% e Investigación y Desarrollo 14.9%.

## 4. Hipótesis a validar

1. El sobretiempo está asociado con mayor probabilidad de turnover, incluso controlando función, edad y salario.
2. Los viajes frecuentes incrementan la probabilidad de turnover, especialmente en puestos con sobretiempo.
3. La tasa superior en colaboradores de 18 a 25 años se explica parcialmente por salario, antigüedad y nivel de trabajo.
4. El bajo balance laboral se relaciona con turnover aun controlando carga, función y compensación.
5. Parte de la diferencia entre funciones responde a la composición de roles, salarios y condiciones de trabajo.

Estas hipótesis requieren análisis inferencial o modelos multivariados; el dashboard por sí solo no confirma causalidad.

## 5. Recomendaciones

1. Revisar carga y sobretiempo por función y rol, priorizando segmentos con mayor tasa y volumen suficiente.
2. Analizar políticas de viajes y recuperación para grupos con alta frecuencia.
3. Profundizar motivos de salida y expectativas de carrera en el grupo de 18 a 25 años.
4. Cruzar balance laboral con manager, antigüedad, satisfacción y carga antes de diseñar una intervención.
5. Complementar con entrevistas, encuestas abiertas y datos longitudinales.
6. Evitar decisiones individuales basadas en perfiles; utilizar la información para medidas agregadas y preventivas.

## 6. Valor de un dashboard descriptivo

Un dashboard consolida métricas, permite segmentar patrones y ayuda a priorizar preguntas de negocio. Su valor no está en demostrar causalidad, sino en facilitar una lectura consistente, identificar focos y orientar análisis posteriores y conversaciones de gestión.
