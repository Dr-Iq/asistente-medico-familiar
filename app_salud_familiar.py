import streamlit as st

# Configuración de la página para que se adapte a pantallas de celular
st.set_page_config(
    page_title="Asistente Médico Familiar",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados para hacer la interfaz atractiva y fácil de usar en celular
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0f4c81 0%, #1b7ced 100%);
        color: white;
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    .main-header h1 {
        color: white !important;
        font-size: 1.7rem !important;
        margin-bottom: 6px;
    }
    .main-header p {
        color: #e2f1ff;
        font-size: 0.95rem;
        margin: 0;
    }
    .card-roja {
        background-color: #fff5f5;
        border-left: 8px solid #e53e3e;
        padding: 18px;
        border-radius: 12px;
        color: #742a2a;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(229,62,62,0.15);
    }
    .card-amarilla {
        background-color: #fffff0;
        border-left: 8px solid #dd6b20;
        padding: 18px;
        border-radius: 12px;
        color: #7b341e;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(221,107,32,0.15);
    }
    .card-verde {
        background-color: #f0fff4;
        border-left: 8px solid #38a169;
        padding: 18px;
        border-radius: 12px;
        color: #22543d;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(56,161,105,0.15);
    }
    .card-med {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        border-left: 6px solid #2563eb;
        padding: 16px;
        border-radius: 12px;
        color: #1e293b;
        margin-bottom: 14px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.4em;
        font-weight: bold;
        font-size: 1.08rem;
        background: linear-gradient(90deg, #1b7ced 0%, #0f4c81 100%);
        color: white;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Encabezado principal
st.markdown("""
<div class="main-header">
    <h1>🩺 Asistente Médico Familiar</h1>
    <p>Orientación de síntomas, dosis pediátricas por peso y prevención en lenguaje claro</p>
</div>
""", unsafe_allow_html=True)

# Creación de pestañas táctiles
tab1, tab2 = st.tabs(["🌡️ Síntomas y Dosis (Niños/Adultos)", "❤️ Riesgo en Años (Diabetes/Presión)"])

# ==============================================================================
# PESTAÑA 1: TRIAJE DE SÍNTOMAS Y CALCULADORA DE DOSIS POR PESO
# ==============================================================================
with tab1:
    st.subheader("1. Datos del Paciente")
    tipo_paciente = st.radio(
        "¿Para quién es la consulta?",
        ["👶 Bebé o Niño (Menor de 15 años)", "🧑 Adulto o Adolescente (15 años o más)"],
        horizontal=True
    )
    es_menor = tipo_paciente.startswith("👶")

    col1, col2 = st.columns(2)
    with col1:
        if es_menor:
            unidad_edad = st.selectbox("Edad en:", ["Años cumplidos", "Meses (Bebé menor de 1 año)"])
            if unidad_edad.startswith("Meses"):
                edad_meses = st.number_input("¿Cuántos meses tiene?", min_value=0, max_value=11, value=6, step=1)
                edad_anos = edad_meses / 12.0
            else:
                edad_anos = st.number_input("¿Cuántos años tiene?", min_value=1, max_value=14, value=5, step=1)
                edad_meses = edad_anos * 12
        else:
            edad_anos = st.number_input("Edad en años:", min_value=15, max_value=110, value=35, step=1)
            edad_meses = edad_anos * 12

    with col2:
        peso_default = 18.0 if es_menor else 70.0
        peso_min = 2.5 if es_menor else 35.0
        peso = st.number_input("Peso en kg (exacto o aprox.):", min_value=peso_min, max_value=220.0, value=peso_default, step=0.5)

    st.divider()
    st.subheader("2. 🚨 Evaluación de Signos de Alarma")
    st.caption("Marca si la persona presenta alguno de estos síntomas en este momento:")

    alarma_resp = st.checkbox("😤 Dificultad para respirar, se le hunden las costillas, le silba el pecho o labios morados")
    alarma_neuro = st.checkbox("😵 Muy decaído (cuesta despertarlo), confundido, convulsiones o cuello rígido")
    alarma_dolor = st.checkbox("🤢 Dolor fuerte en el pecho/abdomen o vómitos que no paran (no retiene líquidos)")
    alarma_piel = st.checkbox("🩸 Manchitas rojas/moradas en la piel que NO se borran al presionar, o sangrados")
    alarma_deshid = st.checkbox("💧 Llora sin lágrimas, boca totalmente seca o lleva más de 8 horas sin orinar")

    st.divider()
    st.subheader("3. Síntomas Actuales")
    tiene_fiebre = st.toggle("🌡️ ¿Tiene fiebre o cuerpo caliente?", value=True)
    if tiene_fiebre:
        c_f1, c_f2 = st.columns(2)
        with c_f1:
            temp = st.slider("Temperatura (°C):", min_value=36.0, max_value=42.0, value=38.5, step=0.1)
        with c_f2:
            dias_fiebre = st.number_input("Días con fiebre:", min_value=1, max_value=30, value=1, step=1)
    else:
        temp = 36.5
        dias_fiebre = 0

    c_s1, c_s2 = st.columns(2)
    with c_s1:
        dolor_muscular = st.checkbox("🤕 Dolor muscular o de cabeza leve", value=True)
        resfriado = st.checkbox("🤧 Escurrimiento nasal o estornudos")
    with c_s2:
        dolor_focal = st.checkbox("👂 Dolor de oído, pus en garganta o ardor al orinar")
        diarrea = st.checkbox("🚽 Diarrea líquida")

    st.divider()
    st.subheader("4. Seguridad de Medicamentos")
    alergia = st.checkbox("⚠️ ¿Tiene alergia al Paracetamol o al Ibuprofeno?")
    riesgo_gastrico_dengue = st.checkbox("⚠️ ¿Padece gastritis/úlcera, enfermedad renal o hay sospecha de Dengue?")

    if st.button("🔍 Evaluar Síntomas y Calcular Dosis"):
        urgencias = []
        consultorio = []

        if es_menor and edad_meses < 3 and temp >= 38.0:
            urgencias.append("Fiebre (38.0 °C o más) en un bebé menor de 3 meses.")
        if temp >= 40.0:
            urgencias.append(f"Fiebre muy elevada ({temp} °C).")
        if alarma_resp:
            urgencias.append("Dificultad para respirar, hundimiento de costillas o falta de aire.")
        if alarma_neuro:
            urgencias.append("Decaimiento extremo, confusión, convulsión o rigidez de cuello.")
        if alarma_dolor:
            urgencias.append("Dolor intenso en pecho/abdomen o vómitos que impiden hidratar.")
        if alarma_piel:
            urgencias.append("Manchas en la piel o sangrados (descartar dengue con alarma o infección severa).")
        if alarma_deshid:
            urgencias.append("Signos de deshidratación importante (más de 8 h sin orinar o boca seca).")

        if not urgencias:
            if dias_fiebre >= 3:
                consultorio.append(f"Lleva {dias_fiebre} días con fiebre (más de 72 horas requiere revisión médica).")
            if es_menor and 3 <= edad_meses < 24 and temp >= 38.5:
                consultorio.append("Menor de 2 años con fiebre mayor a 38.5 °C.")
            if dolor_focal:
                consultorio.append("Dolor de oído, pus en garganta o ardor al orinar (probable infección que requiere receta).")
            if riesgo_gastrico_dengue and tiene_fiebre:
                consultorio.append("Fiebre con sospecha de Dengue o condición médica previa.")

        st.markdown("### 📋 Resultado de la Orientación")

        # NIVEL ROJO
        if urgencias:
            lista_html = "".join([f"<li><b>{u}</b></li>" for u in urgencias])
            st.markdown(f"""
            <div class="card-roja">
                <h3>🚨 ¡ACUDIR INMEDIATAMENTE A URGENCIAS DE UN HOSPITAL!</h3>
                <p>Se detectaron signos de alarma que requieren atención médica inmediata:</p>
                <ul>{lista_html}</ul>
                <p><b>Importante:</b> No esperes en casa ni ocultes los síntomas con medicamentos.</p>
            </div>
            """, unsafe_allow_html=True)

        else:
            # NIVEL AMARILLO O VERDE
            if consultorio:
                lista_c = "".join([f"<li>{c}</li>" for c in consultorio])
                st.markdown(f"""
                <div class="card-amarilla">
                    <h3>⚠️ ACUDIR A CONSULTORIO MÉDICO HOY MISMO</h3>
                    <p>No es una emergencia de hospital en este segundo, pero <b>sí requiere revisión médica</b> por lo siguiente:</p>
                    <ul>{lista_c}</ul>
                    <p>Mientras acudes al médico, puedes aliviar el malestar con las dosis de abajo:</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="card-verde">
                    <h3>✅ SÍNTOMAS LEVES - MANEJO EN CASA CON VIGILANCIA</h3>
                    <p>Parece tratarse de un cuadro leve o viral inicial. Si dura más de 3 días o empeora, acude a consultorio médico.</p>
                </div>
                """, unsafe_allow_html=True)

            # CÁLCULO DE MEDICAMENTOS
            if alergia:
                st.warning("⚠️ Como indicaste alergia a Paracetamol o Ibuprofeno, NO administres medicamento sin consultar a tu médico.")
            elif tiene_fiebre or dolor_muscular:
                st.markdown("#### 💊 Dosis Calculada según el Peso")

                if es_menor and peso < 40.0:
                    mg_para = min(peso * 15.0, 750.0)
                    ml_gotas = mg_para / 100.0
                    gotas = ml_gotas * 20
                    ml_jarabe = (mg_para * 5.0) / 160.0

                    st.markdown(f"""
                    <div class="card-med">
                        <h4>1️⃣ PARACETAMOL (1ª opción más segura para fiebre y dolor)</h4>
                        <p><b>• Dosis exacta para {peso:.1f} kg:</b> {mg_para:.0f} mg cada 6 u 8 horas (Máximo 4 tomas al día).</p>
                        <p><b>• ¿Cuánto darle según el frasco que tengas? (Revisa tu caja):</b></p>
                        <ul>
                            <li><b>Gotero Pediátrico (100 mg / 1 ml):</b> Dar <b>{ml_gotas:.1f} ml</b> (aprox. {gotas:.0f} gotas).</li>
                            <li><b>Jarabe Infantil (160 mg / 5 ml o 3.2 g/100ml):</b> Dar <b>{ml_jarabe:.1f} ml</b> con jeringa medidora.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

                    if edad_meses < 6:
                        st.info("ℹ️ **IBUPROFENO:** No se debe administrar en bebés menores de 6 meses.")
                    elif diarrea or riesgo_gastrico_dengue:
                        st.warning("⚠️ **IBUPROFENO:** Evítalo en esta ocasión. Con diarrea, gastritis o sospecha de Dengue solo se debe usar Paracetamol.")
                    else:
                        mg_ibu = min(peso * 10.0, 400.0)
                        ml_ibu_100 = (mg_ibu * 5.0) / 100.0
                        ml_ibu_200 = (mg_ibu * 5.0) / 200.0
                        st.markdown(f"""
                        <div class="card-med">
                            <h4>2️⃣ IBUPROFENO (Alternativa desinflamatoria, dar con alimentos)</h4>
                            <p><b>• Dosis exacta para {peso:.1f} kg:</b> {mg_ibu:.0f} mg cada 8 horas (No dar junto con Paracetamol).</p>
                            <ul>
                                <li><b>Suspensión Infantil (100 mg / 5 ml o 2 g/100ml):</b> Dar <b>{ml_ibu_100:.1f} ml</b>.</li>
                                <li><b>Suspensión Pediátrica (200 mg / 5 ml o 4 g/100ml):</b> Dar <b>{ml_ibu_200:.1f} ml</b>.</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="card-med">
                        <h4>1️⃣ PARACETAMOL (Tabletas 500 mg)</h4>
                        <p><b>• Dosis:</b> 1 tableta de 500 mg (o hasta 2 tabletas si el dolor/fiebre es fuerte y pesas más de 60 kg) cada 6 u 8 horas.</p>
                        <p><i>Nota: Nunca exceder 6 tabletas de 500 mg (3,000 mg) en 24 horas.</i></p>
                    </div>
                    """, unsafe_allow_html=True)

                    if diarrea or riesgo_gastrico_dengue:
                        st.warning("⚠️ **IBUPROFENO / NAPROXENO / ASPIRINA:** Evítalos por el riesgo gástrico, diarrea o sospecha de Dengue. Usa solo Paracetamol.")
                    else:
                        st.markdown("""
                        <div class="card-med">
                            <h4>2️⃣ IBUPROFENO (Tabletas/Cápsulas 400 mg - Alternativa)</h4>
                            <p><b>• Dosis:</b> 1 tableta de 400 mg cada 8 horas siempre después de algún alimento (por máximo 3 días).</p>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("#### 💧 Cuidados en Casa")
            if tiene_fiebre:
                st.write("• **Para la fiebre:** Ropa ligera, habitación fresca y beber líquidos constantemente. No uses alcohol ni agua helada.")
            if diarrea:
                st.write("• **Para la diarrea:** Vida Suero Oral a pequeños sorbos después de cada evacuación. Evita refrescos y jugos dulces.")
            if resfriado:
                st.write("• **Congestión:** Lavados nasales con spray de agua de mar (solución salina).")
            st.write("• **Regla de seguridad:** Nunca des Aspirina (ácido acetilsalicílico) ni antibióticos sin receta médica.")


# ==============================================================================
# PESTAÑA 2: EVALUADOR DE RIESGO METABÓLICO Y PROYECCIÓN EN AÑOS
# ==============================================================================
with tab2:
    st.subheader("1. Tus Medidas Básicas")
    c1, c2 = st.columns(2)
    with c1:
        sexo_m = st.selectbox("Sexo biológico:", ["Masculino", "Femenino"])
        edad_m = st.number_input("Tu edad:", min_value=10, max_value=110, value=38)
        peso_nacer = st.selectbox("Tu peso al nacer:", ["Normal (2.5 a 4 kg) o no sé", "Bajo peso (< 2.5 kg)", "Mucho peso (> 4.0 kg)"])
    with c2:
        peso_m = st.number_input("Tu peso actual (kg):", min_value=25.0, max_value=250.0, value=78.0, step=0.5)
        talla_m = st.number_input("Tu estatura (cm):", min_value=110.0, max_value=230.0, value=168.0, step=1.0)
        cintura_m = st.number_input("Tu cintura al ombligo (cm):", min_value=45.0, max_value=200.0, value=93.0, step=1.0)

    st.divider()
    st.subheader("2. Historial Familiar y Personal")
    fam_dm = st.selectbox("¿Familiares con Diabetes Tipo 2?", ["No", "Sí: abuelos, tíos o primos", "Sí: padres, hermanos o hijos"])
    fam_hta = st.checkbox("¿Padres o hermanos con Presión Arterial Alta?")
    fam_ob = st.checkbox("¿Padres o hermanos con Obesidad?")
    glucosa_previa = st.checkbox("¿Alguna vez te detectaron el azúcar un poco alta?")
    hta_previa = st.checkbox("¿Te han detectado presión alta o tomas medicamento para la presión?")

    st.divider()
    st.subheader("3. Hábitos, Sueño y Estrés")
    ch1, ch2 = st.columns(2)
    with ch1:
        ejercicio = st.checkbox("🏃 Hago al menos 30 min de ejercicio diario", value=True)
        vegetales = st.checkbox("🥗 Como verduras o ensalada todos los días")
        ultraprocesados = st.checkbox("🥤 Tomo refrescos, pan dulce o comida rápida >= 3 veces/semana", value=True)
        sodio = st.checkbox("🧂 Pongo sal extra o como embutidos casi diario")
    with ch2:
        sueno_corto = st.checkbox("😴 Duermo menos de 6 horas por noche", value=True)
        estres = st.checkbox("🤯 Vivo con estrés fuerte casi todos los días", value=True)
        apnea = st.checkbox("💤 Ronco fuerte o dejo de respirar al dormir")
        tabaco_alcohol = st.checkbox("🚬 Fumo o bebo alcohol con frecuencia")

    if st.button("📊 Calcular Mi Riesgo en los Próximos Años"):
        imc = peso_m / ((talla_m / 100.0) ** 2)
        ice = cintura_m / talla_m
        cintura_meta = talla_m / 2.0

        # Puntaje Diabetes
        pts_dm = 0
        if 45 <= edad_m <= 54: pts_dm += 2
        elif 55 <= edad_m <= 64: pts_dm += 3
        elif edad_m > 64: pts_dm += 4

        if 25 <= imc < 30: pts_dm += 1
        elif imc >= 30: pts_dm += 3

        limite_cint = 90 if sexo_m == "Masculino" else 80
        limite_alto = 102 if sexo_m == "Masculino" else 88
        if limite_cint <= cintura_m <= limite_alto: pts_dm += 3
        elif cintura_m > limite_alto: pts_dm += 4

        if not ejercicio: pts_dm += 2
        if not vegetales: pts_dm += 1
        if hta_previa: pts_dm += 2
        if glucosa_previa: pts_dm += 5
        if "abuelos" in fam_dm: pts_dm += 3
        elif "padres" in fam_dm: pts_dm += 5
        if ultraprocesados: pts_dm += 2
        if sueno_corto or apnea: pts_dm += 1
        if not peso_nacer.startswith("Normal"): pts_dm += 1

        if pts_dm < 7:
            res_dm = ("BAJO", "1% en los próximos 10 años (1 de cada 100)", "Sin riesgo cercano si mantienes tus hábitos.")
        elif pts_dm <= 11:
            res_dm = ("LIGERAMENTE ELEVADO", "4% en los próximos 10 años (1 de cada 25)", "Podría aparecer en 8 a 10 años si aumentan los descuidos.")
        elif pts_dm <= 14:
            res_dm = ("MODERADO", "17% en los próximos 10 años (1 de cada 6)", "Sin cambios, puede aparecer prediabetes o diabetes en 5 a 8 años.")
        elif pts_dm <= 20:
            res_dm = ("ALTO", "33% en los próximos 10 años (1 de cada 3)", "¡Atención! Sin cambios, puede manifestarse en 3 a 5 años.")
        else:
            res_dm = ("MUY ALTO", "50% o más en los próximos 10 años (1 de cada 2)", "¡Urgente! Alta probabilidad en 1 a 3 años (hazte un chequeo pronto).")

        # Puntaje Hipertensión
        pts_hta = 10 if hta_previa else 0
        if (sexo_m == "Masculino" and edad_m >= 45) or (sexo_m == "Femenino" and edad_m >= 55): pts_hta += 2
        if fam_hta: pts_hta += 3
        if imc >= 30 or ice >= 0.55: pts_hta += 3
        elif imc >= 25 or ice >= 0.50: pts_hta += 1
        if sodio: pts_hta += 2
        if not vegetales: pts_hta += 1
        if tabaco_alcohol: pts_hta += 3
        if apnea: pts_hta += 3
        if estres or sueno_corto: pts_hta += 2
        if not ejercicio: pts_hta += 1

        if hta_previa:
            res_hta = ("CONDICIÓN YA PRESENTE", "Ya tienes antecedente de presión alta", "Requiere control actual para proteger corazón y riñones.")
        elif pts_hta <= 3:
            res_hta = ("BAJO", "Menos del 5% en los próximos 5 a 10 años", "Tus arterias tienen poca carga de estrés.")
        elif pts_hta <= 7:
            res_hta = ("MODERADO", "15% a 25% en los próximos 5 a 10 años (1 de cada 5)", "De seguir con el mismo estrés/hábitos, puede subir en 5 a 8 años.")
        elif pts_hta <= 11:
            res_hta = ("ALTO", "35% a 50% en los próximos 5 años (1 de cada 2 o 3)", "Sin cambios, puedes desarrollar hipertensión en 2 a 5 años.")
        else:
            res_hta = ("MUY ALTO", "Más del 60% en los próximos 3 a 5 años", "Alta probabilidad de aparecer en 1 a 3 años.")

        # Puntaje Obesidad
        if imc >= 30:
            res_ob = ("OBESIDAD ESTABLECIDA", f"Tu IMC actual es {imc:.1f} kg/m²", "Riesgo de inflamar el hígado en 1 a 3 años si no se reduce cintura.")
        elif ice >= 0.50:
            res_ob = ("GRASA ABDOMINAL ACTIVA", "35% a 50% de pasar a Obesidad General en 3 a 5 años", "Ya tienes grasa 'inquieta' (visceral) en el abdomen hoy mismo.")
        else:
            res_ob = ("BAJO", "Menos del 5% en los próximos 5 años", "Tu cintura mide menos de la mitad de tu estatura. ¡Excelente!")

        st.markdown("### 📊 Tu Proyección de Salud en Palabras Sencillas")

        if ice >= 0.50:
            bajar_cm = cintura_m - (cintura_meta - 1)
            st.warning(f"📏 **Relación Cintura/Estatura ({ice:.2f}):** Tu cintura mide **{cintura_m:.0f} cm** y rebasa la mitad de tu estatura ({cintura_meta:.0f} cm). Si bajas unos **{bajar_cm:.0f} cm** de barriga, tu riesgo se reducirá a menos de la mitad.")
        else:
            st.success(f"📏 **Relación Cintura/Estatura ({ice:.2f}):** ¡Felicidades! Tu cintura mide menos de la mitad de tu estatura ({cintura_meta:.0f} cm).")

        if sueno_corto and estres and ultraprocesados:
            st.info("💡 **¿Qué pasa en tu cuerpo? (El círculo del cansancio):** Como duermes poco y tienes mucho estrés, tu hormona de alerta (cortisol) amanece alta y tus hormonas del hambre se disparan. Por eso tu cerebro te pide pan, azúcar o refrescos para aguantar el día, y el estrés guarda esa energía directo en tu abdomen.")

        for nombre, (nivel, prob, tiempo) in [
            ("🩸 1. DIABETES TIPO 2 (Azúcar)", res_dm),
            ("❤️ 2. HIPERTENSIÓN ARTERIAL (Presión)", res_hta),
            ("⚖️ 3. OBESIDAD Y GRASA EN EL ABDOMEN", res_ob)
        ]:
            clase = "card-verde" if "BAJO" in nivel else ("card-amarilla" if "MODERADO" in nivel or "LIGERAMENTE" in nivel else "card-roja")
            st.markdown(f"""
            <div class="{clase}">
                <h4>{nombre}: {nivel}</h4>
                <p><b>• Probabilidad:</b> {prob}</p>
                <p><b>• Tiempo estimado:</b> {tiempo}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### 🎯 Tus 3 Cambios más Efectivos (Sin dietas extremas)")
        if sueno_corto:
            st.write("1. **Duerme 45 a 60 min más:** Apagarás la hormona del hambre (grelina) y tendrás muchos menos antojos dulces al día siguiente.")
        if ultraprocesados:
            st.write("2. **Cambia refrescos/jugos entre semana por agua mineral con limón:** Es la vía más rápida para desinflamar la barriga.")
        if not vegetales or ice >= 0.50:
            st.write("3. **El truco del orden en el plato:** Empieza siempre comiendo verduras o ensalada antes del plato fuerte para frenar el pico de azúcar.")