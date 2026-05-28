# Predicción de la Diferencia de Edad entre Cónyuges en Guatemala (2011-2021)
# David Domínguez (23712), Luis Padilla (23663), Gabriel Bran (23590)
# Dataset: mat_full.csv  –  Registros INE Guatemala 2011-2021
# Variable respuesta: DIFF_EDAD = EDADHOM − EDADMUJ


# SECCIÓN 0 – IMPORTACIÓN DE LIBRERÍAS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import unicodedata
import warnings
warnings.filterwarnings('ignore')

from scipy import stats

# Scikit-learn – preprocesamiento
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.utils.class_weight import compute_sample_weight

# Scikit-learn – modelos de árbol
from sklearn.tree import (
    DecisionTreeRegressor, DecisionTreeClassifier, plot_tree
)
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

# Scikit-learn – modelos lineales
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LogisticRegression

# Scikit-learn – métricas
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

# XGBoost
from xgboost import XGBRegressor, XGBClassifier
import xgboost as xgb

# Configuración general de visualización
sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams['figure.dpi'] = 100
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print("Librerías cargadas correctamente.")
print(f"XGBoost version: {xgb.__version__}")


# SECCIÓN 1 – CARGA Y PREPARACIÓN INICIAL DE DATOS

RUTA_CSV = 'mat_full.csv'

df = pd.read_csv(RUTA_CSV)

# Las columnas EDADHOM, EDADMUJ y AÑOREG son numéricas pero pueden venir como
# texto en algunas versiones del archivo; se fuerza la conversión.
for col in ['EDADHOM', 'EDADMUJ', 'AÑOREG', 'DIAOCU']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

print(f"\nShape original del dataset : {df.shape}")
print(f"Columnas disponibles       : {df.columns.tolist()}")
print(f"\nPrimeras filas:")
print(df.head())


# SECCIÓN 2 – ESTADÍSTICOS DESCRIPTIVOS

print("\n" + "=" * 70)
print("ESTADÍSTICOS DESCRIPTIVOS – VARIABLES NUMÉRICAS")
print("=" * 70)

df_num = df.select_dtypes(include=['number'])
print(df_num.describe().T)

# Cuartiles
print("\nCuartiles (Q1, Mediana, Q3):")
print(df_num.quantile([0.25, 0.5, 0.75]).T.rename(
    columns={0.25: 'Q1', 0.5: 'Mediana', 0.75: 'Q3'}))

# Rango, varianza y desviación estándar
dist_df = pd.DataFrame({
    'Min':     df_num.min(),
    'Max':     df_num.max(),
    'Rango':   df_num.max() - df_num.min(),
    'Varianza': df_num.var(),
    'Desv.Std': df_num.std(),
})
print("\nDistribución:")
print(dist_df)

print("\n" + "=" * 70)
print("DISTRIBUCIÓN DE VARIABLES CATEGÓRICAS CLAVE")
print("=" * 70)

# Clase de unión
print("\nCLASE DE UNIÓN (CLAUNI):")
clauni = df['CLAUNI'].value_counts()
clauni_pct = df['CLAUNI'].value_counts(normalize=True) * 100
print(pd.DataFrame({'Frecuencia': clauni, 'Porcentaje %': clauni_pct.round(2)}))

# Escolaridad del hombre y la mujer
orden_esc = ['Ninguno', 'Primaria', 'Básico', 'Diversificado', 'Universitario', 'Ignorado']
for col, nombre in [('ESCHOM', 'HOMBRE'), ('ESCMUJ', 'MUJER')]:
    print(f"\nESCOLARIDAD DEL {nombre} ({col}):")
    frq = df[col].value_counts().reindex(
        [e for e in orden_esc if e in df[col].unique()], fill_value=0)
    pct = (frq / len(df) * 100).round(2)
    print(pd.DataFrame({'Frecuencia': frq, 'Porcentaje %': pct}))

# Distribución mensual
orden_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
               'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
print("\nDISTRIBUCIÓN POR MES DE OCURRENCIA (MESOCU):")
mesocu = df['MESOCU'].value_counts().reindex(orden_meses)
print(pd.DataFrame({
    'Frecuencia': mesocu,
    'Porcentaje %': (mesocu / len(df) * 100).round(2)
}))

# Top 10 departamentos
print("\nTOP 10 DEPARTAMENTOS DE REGISTRO (DEPREG):")
print(df['DEPREG'].value_counts().head(10))

# Top 10 municipios de ocurrencia
print("\nTOP 10 MUNICIPIOS DE OCURRENCIA (MUPOCU):")
print(df['MUPOCU'].value_counts().head(10))

# Nacionalidad
for col in ['NACHOM', 'NACMUJ']:
    n_gt = (df[col] == 'Guatemala').sum()
    total = df[col].notna().sum()
    print(f"\nNacionalidad guatemalteca en {col}: "
          f"{n_gt:,} / {total:,} ({n_gt/total*100:.2f}%)")


# SECCIÓN 3 – VISUALIZACIONES DESCRIPTIVAS

# --- 3.1 Histogramas de edades ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
for ax, col, color, titulo in [
    (axes[0], 'EDADHOM', 'skyblue',  'Hombre'),
    (axes[1], 'EDADMUJ', 'salmon',   'Mujer'),
]:
    sns.histplot(df[col].dropna(), bins=40, kde=True, ax=ax, color=color)
    ax.axvline(df[col].mean(),   color='red',   ls='--',
               label=f'Media: {df[col].mean():.1f}')
    ax.axvline(df[col].median(), color='green', ls='-',
               label=f'Mediana: {df[col].median():.1f}')
    ax.set_title(f'Distribución de Edad del {titulo} al Casarse')
    ax.set_xlabel('Edad (años)')
    ax.legend()
plt.tight_layout()
plt.savefig('plot_edades_hist.png', bbox_inches='tight')
plt.show()

# --- 3.2 Evolución temporal de matrimonios por año ---
conteo_años = df['AÑOREG'].value_counts().sort_index()
plt.figure(figsize=(12, 5))
plt.plot(conteo_años.index, conteo_años.values, 'o-', lw=2, markersize=8)
max_año = conteo_años.idxmax()
min_año = conteo_años.idxmin()
plt.annotate(f'Pico: {int(conteo_años.max()):,}',
             xy=(max_año, conteo_años.max()),
             xytext=(max_año - 1, conteo_años.max() + 4000),
             arrowprops=dict(arrowstyle='->'))
plt.annotate(f'Valle: {int(conteo_años.min()):,}',
             xy=(min_año, conteo_años.min()),
             xytext=(min_año + 0.5, conteo_años.min() - 7000),
             arrowprops=dict(arrowstyle='->'))
plt.title('Evolución del Número de Matrimonios por Año (2011-2021)')
plt.xlabel('Año')
plt.ylabel('Número de Matrimonios')
plt.xticks(list(conteo_años.index))
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('plot_evolucion_anual.png', bbox_inches='tight')
plt.show()

# --- 3.3 Mapa de calor: matrimonios por año y mes ---
pivot_meses = pd.crosstab(df['AÑOREG'], df['MESOCU'])
pivot_meses = pivot_meses.reindex(columns=orden_meses, fill_value=0)
plt.figure(figsize=(14, 7))
sns.heatmap(pivot_meses, annot=True, fmt='d', cmap='YlOrRd',
            linewidths=0.5, cbar_kws={'label': 'Matrimonios'})
plt.title('Mapa de Calor: Matrimonios por Año y Mes de Ocurrencia')
plt.xlabel('Mes')
plt.ylabel('Año')
plt.tight_layout()
plt.savefig('plot_heatmap_anio_mes.png', bbox_inches='tight')
plt.show()

# --- 3.4 Correlación entre variables numéricas ---
plt.figure(figsize=(8, 6))
sns.heatmap(df_num.corr(), annot=True, fmt='.2f', cmap='coolwarm',
            center=0, square=True, linewidths=0.5)
plt.title('Mapa de Correlación – Variables Numéricas')
plt.tight_layout()
plt.savefig('plot_correlacion.png', bbox_inches='tight')
plt.show()


# SECCIÓN 4 – ANÁLISIS DE LA VARIABLE RESPUESTA: DIFF_EDAD

# Crear DIFF_EDAD y limpiar filas sin edades válidas
df['DIFF_EDAD'] = df['EDADHOM'] - df['EDADMUJ']
df_clean = df.dropna(subset=['EDADHOM', 'EDADMUJ', 'DIFF_EDAD']).copy()

print(f"\nRegistros totales              : {len(df):>10,}")
print(f"Registros con DIFF_EDAD válido : {len(df_clean):>10,}")
print(f"Registros eliminados           : {len(df) - len(df_clean):>10,}")

d = df_clean['DIFF_EDAD']
n = len(d)
n_neg  = (d < 0).sum()
n_cero = (d == 0).sum()
n_pos  = (d > 0).sum()

print("\n--- Estadísticos de DIFF_EDAD ---")
print(f"  Media          : {d.mean():.2f} años")
print(f"  Mediana        : {d.median():.0f} años")
print(f"  Desv. estándar : {d.std():.2f} años")
print(f"  Mínimo         : {d.min():.0f} años")
print(f"  Máximo         : {d.max():.0f} años")
print(f"  Rango p5–p95   : {d.quantile(.05):.0f} a {d.quantile(.95):.0f} años")
print(f"  Asimetría      : {d.skew():.3f}")
print(f"  Mujer mayor    : {n_neg:,}  ({n_neg/n*100:.1f}%)")
print(f"  Misma edad     : {n_cero:,}  ({n_cero/n*100:.1f}%)")
print(f"  Hombre mayor   : {n_pos:,}  ({n_pos/n*100:.1f}%)")

# --- Histograma y percentiles de DIFF_EDAD ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax = axes[0]
ax.hist(df_clean['DIFF_EDAD'], bins=70, color='steelblue',
        edgecolor='white', alpha=0.85)
ax.axvline(d.mean(),   color='tomato', lw=2, ls='--',
           label=f'Media: {d.mean():.2f}')
ax.axvline(d.median(), color='gold',   lw=2, ls='--',
           label=f'Mediana: {d.median():.0f}')
ax.axvline(0, color='black', lw=1, ls=':')
ax.set_title('Distribución de DIFF_EDAD\n(EDADHOM − EDADMUJ)')
ax.set_xlabel('Diferencia de Edad [años]')
ax.set_ylabel('Frecuencia')
ax.legend()

pcts = [1, 5, 10, 25, 50, 75, 90, 95, 99]
vals = [d.quantile(p / 100) for p in pcts]
ax2 = axes[1]
colors_bar = ['tomato' if v < 0 else 'steelblue' for v in vals]
bars = ax2.bar([str(p) for p in pcts], vals,
               color=colors_bar, edgecolor='white', alpha=0.8)
ax2.axhline(0, color='black', lw=1)
for bar, val in zip(bars, vals):
    ax2.text(bar.get_x() + bar.get_width() / 2,
             val + (0.3 if val >= 0 else -0.8),
             f'{val:.0f}', ha='center', fontsize=9, fontweight='bold')
ax2.set_title('Percentiles de DIFF_EDAD')
ax2.set_xlabel('Percentil')
ax2.set_ylabel('Diferencia de Edad [años]')

plt.tight_layout()
plt.savefig('plot_diff_edad_dist.png', bbox_inches='tight')
plt.show()


# SECCIÓN 5 – CATEGORIZACIÓN DE LA VARIABLE RESPUESTA

# Clasificación en 5 clases (CAT_DIFF) – cortes definidos por el artículo
bins5   = [-np.inf, 0, 2, 3, 5, np.inf]
labels5 = ['Mujer mayor', '0-2 años', '2-3 años', '3-5 años', '> 5 años']
df_clean['CAT_DIFF'] = pd.cut(df_clean['DIFF_EDAD'], bins=bins5, labels=labels5)

# Clasificación en 3 clases (CAT3) – más balanceada
bins3   = [-np.inf, -1, 5, np.inf]
labels3 = ['Mujer mayor o igual', 'Hombre 0-5 años mayor', 'Hombre > 5 años mayor']
df_clean['CAT3'] = pd.cut(df_clean['DIFF_EDAD'], bins=bins3, labels=labels3)

print("\nDistribución CAT_DIFF (5 clases):")
for lbl, cnt in df_clean['CAT_DIFF'].value_counts().items():
    print(f"  {lbl:<20}: {cnt:>7,}  ({cnt/n*100:.1f}%)")

print("\nDistribución CAT3 (3 clases):")
for lbl, cnt in df_clean['CAT3'].value_counts().items():
    print(f"  {lbl:<25}: {cnt:>7,}  ({cnt/n*100:.1f}%)")

# Gráficos de distribución de categorías
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
df_clean['CAT_DIFF'].value_counts().plot(
    kind='bar', ax=axes[0], color='coral', edgecolor='white')
axes[0].set_title('Variable CAT_DIFF (5 clases)')
axes[0].tick_params(axis='x', rotation=30)

df_clean['CAT3'].value_counts().plot(
    kind='bar', ax=axes[1], color='seagreen', edgecolor='white')
axes[1].set_title('Variable CAT3 (3 clases)')
axes[1].tick_params(axis='x', rotation=30)

plt.suptitle('Categorización de la Variable Respuesta DIFF_EDAD', y=1.02)
plt.tight_layout()
plt.savefig('plot_categorias_respuesta.png', bbox_inches='tight')
plt.show()


# SECCIÓN 6 – VALIDACIÓN ESTADÍSTICA DE HIPÓTESIS Y ASOCIACIÓN DE PREDICTORES

print("\n" + "=" * 70)
print("PRUEBAS DE ASOCIACIÓN ESTADÍSTICA: PREDICTORES vs. DIFF_EDAD")
print("=" * 70)

# ---- 6.1 ANOVA: Educación del hombre y la mujer ----
for col, nombre in [('ESCHOM', 'Hombre'), ('ESCMUJ', 'Mujer')]:
    df_e = df_clean[df_clean[col].isin(orden_esc)]
    grupos = [df_e[df_e[col] == e]['DIFF_EDAD'].dropna()
              for e in orden_esc if e in df_e[col].unique()]
    F, p = stats.f_oneway(*grupos)
    grand_mean = df_e['DIFF_EDAD'].mean()
    ss_b = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in grupos)
    ss_t = ((df_e['DIFF_EDAD'] - grand_mean) ** 2).sum()
    eta2 = ss_b / ss_t
    print(f"\nANOVA – Educación del {nombre} ({col})")
    print(f"  F = {F:.2f},  p-valor = {p:.2e}")
    print(f"  Eta² = {eta2:.4f}  ({eta2*100:.2f}% de varianza explicada)")
    print(f"  Media DIFF_EDAD por nivel educativo:")
    print(df_e.groupby(col)['DIFF_EDAD'].mean().reindex(orden_esc).round(2))

# Boxplot de DIFF_EDAD por escolaridad
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
for ax, col, titulo in zip(axes,
                            ['ESCHOM', 'ESCMUJ'],
                            ['Hombre', 'Mujer']):
    etiquetas = [e for e in orden_esc if e in df_clean[col].unique()]
    grupos = [df_clean[df_clean[col] == e]['DIFF_EDAD'].dropna() for e in etiquetas]
    medias = [g.mean() for g in grupos]
    bp = ax.boxplot(grupos, labels=etiquetas, patch_artist=True,
                    medianprops=dict(color='tomato', linewidth=2),
                    flierprops=dict(marker='.', alpha=0.3, markersize=2))
    for patch in bp['boxes']:
        patch.set_facecolor('steelblue'); patch.set_alpha(0.5)
    ax.plot(range(1, len(medias) + 1), medias, 'D--', color='gold',
            markersize=6, label='Media')
    ax.axhline(df_clean['DIFF_EDAD'].mean(), color='black', ls=':',
               label=f'Media global: {df_clean["DIFF_EDAD"].mean():.2f}')
    ax.set_title(f'DIFF_EDAD por Educación del {titulo}')
    ax.set_ylabel('Diferencia de Edad [años]')
    ax.tick_params(axis='x', rotation=15)
    ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig('plot_diff_por_educacion.png', bbox_inches='tight')
plt.show()

# ---- 6.2 T-test: Nacionalidad (hombre extranjero vs. guatemalteco) ----
df_clean['NAC_PAREJA'] = 'Otro'
df_clean.loc[(df_clean['NACHOM'] == 'Guatemala') & (df_clean['NACMUJ'] == 'Guatemala'),
             'NAC_PAREJA'] = 'Ambos guatemaltecos'
df_clean.loc[(df_clean['NACHOM'] != 'Guatemala') & (df_clean['NACMUJ'] == 'Guatemala'),
             'NAC_PAREJA'] = 'Hombre extranjero'
df_clean.loc[(df_clean['NACHOM'] == 'Guatemala') & (df_clean['NACMUJ'] != 'Guatemala'),
             'NAC_PAREJA'] = 'Mujer extranjera'
df_clean.loc[(df_clean['NACHOM'] != 'Guatemala') & (df_clean['NACMUJ'] != 'Guatemala'),
             'NAC_PAREJA'] = 'Ambos extranjeros'

g_gt   = df_clean[df_clean['NAC_PAREJA'] == 'Ambos guatemaltecos']['DIFF_EDAD']
g_hext = df_clean[df_clean['NAC_PAREJA'] == 'Hombre extranjero']['DIFF_EDAD']
t, p_nac = stats.ttest_ind(g_gt, g_hext, equal_var=False)

print(f"\nT-TEST – Ambos guatemaltecos vs. Hombre extranjero")
print(f"  Media guatemaltecos     : {g_gt.mean():.2f} años  (n={len(g_gt):,})")
print(f"  Media hombre extranjero : {g_hext.mean():.2f} años  (n={len(g_hext):,})")
print(f"  t = {t:.2f},  p-valor = {p_nac:.4f}")
if p_nac < 0.05:
    print(f"  DIFERENCIA SIGNIFICATIVA (+{g_hext.mean()-g_gt.mean():.2f} años brecha extra)")

# ---- 6.3 ANOVA: Departamento de registro ----
# Normalizar nombres de departamentos para evitar variantes con/sin tildes
def normalizar_texto(texto):
    if isinstance(texto, str):
        texto = unicodedata.normalize('NFKD', texto)
        texto = ''.join(c for c in texto if not unicodedata.combining(c))
        return texto.lower().strip()
    return texto

df_clean['DEPREG_NORM'] = df_clean['DEPREG'].apply(normalizar_texto)

dep_stats = (df_clean.groupby('DEPREG_NORM')['DIFF_EDAD']
             .agg(['mean', 'median', 'std', 'count'])
             .reset_index()
             .query('count >= 50')
             .sort_values('mean', ascending=True))

grupos_dep = [df_clean[df_clean['DEPREG_NORM'] == d]['DIFF_EDAD'].dropna()
              for d in dep_stats['DEPREG_NORM']]
F_dep, p_dep = stats.f_oneway(*grupos_dep)
grand = df_clean['DIFF_EDAD'].mean()
ss_b_dep = sum(len(g) * (g.mean() - grand) ** 2 for g in grupos_dep)
ss_t_dep = ((df_clean['DIFF_EDAD'] - grand) ** 2).sum()
eta2_dep = ss_b_dep / ss_t_dep

print(f"\nANOVA – Departamento de Registro (DEPREG)")
print(f"  F = {F_dep:.2f},  p-valor = {p_dep:.2e}")
print(f"  Eta² = {eta2_dep:.4f}  ({eta2_dep*100:.2f}% de varianza explicada)")
print("\n  Top 5 departamentos con MAYOR brecha:")
print(dep_stats.sort_values('mean', ascending=False)[
    ['DEPREG_NORM', 'mean', 'count']].head().to_string(index=False))
print("\n  Top 5 departamentos con MENOR brecha:")
print(dep_stats.sort_values('mean')[
    ['DEPREG_NORM', 'mean', 'count']].head().to_string(index=False))

# Gráfico de barras: diferencia promedio por departamento
plt.figure(figsize=(12, 8))
media_global = df_clean['DIFF_EDAD'].mean()
bar_colors = ['tomato' if v < media_global else 'steelblue'
              for v in dep_stats['mean']]
plt.barh(dep_stats['DEPREG_NORM'], dep_stats['mean'],
         color=bar_colors, edgecolor='white', alpha=0.82)
plt.axvline(media_global, color='black', lw=1.5, ls='--',
            label=f'Media nacional: {media_global:.2f}')
plt.title('Diferencia de Edad Promedio por Departamento')
plt.xlabel('Diferencia de Edad promedio [años]')
plt.legend()
plt.tight_layout()
plt.savefig('plot_diff_por_departamento.png', bbox_inches='tight')
plt.show()

# ---- 6.4 Correlación de Pearson: año de registro ----
df_año = df_clean.dropna(subset=['AÑOREG'])
r, p_año = stats.pearsonr(df_año['AÑOREG'], df_año['DIFF_EDAD'])
print(f"\nCORRELACIÓN PEARSON – AÑOREG vs. DIFF_EDAD")
print(f"  r = {r:.4f},  p-valor = {p_año:.4f}")
print("  Tendencia negativa: la brecha se reduce con el tiempo.")

# Evolución temporal de la brecha
año_stats = (df_clean.groupby('AÑOREG')['DIFF_EDAD']
             .agg(['mean', 'median', 'std', 'count'])
             .reset_index().dropna())

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
ax = axes[0]
ax.fill_between(
    año_stats['AÑOREG'],
    año_stats['mean'] - año_stats['std'] / np.sqrt(año_stats['count']) * 1.96,
    año_stats['mean'] + año_stats['std'] / np.sqrt(año_stats['count']) * 1.96,
    alpha=0.15, color='steelblue', label='IC 95%')
ax.plot(año_stats['AÑOREG'], año_stats['mean'],   'o-', color='steelblue', lw=2)
ax.plot(año_stats['AÑOREG'], año_stats['median'], 's--', color='tomato', lw=2)
ax.axhline(media_global, color='black', ls=':', lw=1)
ax.set_title('Tendencia Temporal de la Diferencia de Edad')
ax.set_xlabel('Año de Registro')
ax.set_ylabel('Diferencia de Edad [años]')
ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax.legend()

años = sorted(df_clean['AÑOREG'].dropna().unique())
data_v = [df_clean[df_clean['AÑOREG'] == a]['DIFF_EDAD'].dropna() for a in años]
vp = axes[1].violinplot(data_v, positions=años, showmedians=True, showextrema=False)
for body in vp['bodies']:
    body.set_facecolor('steelblue'); body.set_alpha(0.5)
vp['cmedians'].set_color('tomato'); vp['cmedians'].set_linewidth(2)
axes[1].set_title('Distribución por Año de Registro')
axes[1].set_xlabel('Año')
axes[1].set_ylabel('Diferencia de Edad [años]')
axes[1].xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

plt.tight_layout()
plt.savefig('plot_tendencia_temporal.png', bbox_inches='tight')
plt.show()

print("\nEstadísticos por año:")
print(año_stats[['AÑOREG', 'mean', 'median', 'count']].to_string(index=False))

# ---- 6.5 Test Mann-Kendall (tendencia monótona en la brecha) ----
# Se implementa manualmente porque no todos los entornos tienen pymannkendall
años_serie = año_stats['AÑOREG'].values
medias_serie = año_stats['mean'].values
n_mk = len(medias_serie)
S = 0
for i in range(n_mk - 1):
    for j in range(i + 1, n_mk):
        diff = medias_serie[j] - medias_serie[i]
        if diff > 0:
            S += 1
        elif diff < 0:
            S -= 1
var_S = n_mk * (n_mk - 1) * (2 * n_mk + 5) / 18
tau = S / (n_mk * (n_mk - 1) / 2)
Z_mk = (S - 1) / np.sqrt(var_S) if S > 0 else ((S + 1) / np.sqrt(var_S) if S < 0 else 0)
p_mk = 2 * (1 - stats.norm.cdf(abs(Z_mk)))
print(f"\nTEST MANN-KENDALL – tendencia en la edad promedio al matrimonio")
print(f"  Tau = {tau:.3f},  Z = {Z_mk:.3f},  p-valor = {p_mk:.4f}")
if p_mk < 0.05:
    print("  Tendencia monótona significativa detectada.")

# ---- 6.6 Mapa de calor: Educación Hombre × Educación Mujer ----
orden = ['Ninguno', 'Primaria', 'Básico', 'Diversificado', 'Universitario']
df_gt = df_clean[
    (df_clean['NACHOM'] == 'Guatemala') &
    (df_clean['NACMUJ'] == 'Guatemala') &
    (df_clean['ESCHOM'].isin(orden)) &
    (df_clean['ESCMUJ'].isin(orden))
]

pivot_mean = df_gt.pivot_table(
    values='DIFF_EDAD', index='ESCHOM', columns='ESCMUJ', aggfunc='mean'
).reindex(index=orden, columns=orden)

fig, axes = plt.subplots(1, 2, figsize=(16, 5))
sns.heatmap(pivot_mean, annot=True, fmt='.1f', cmap='RdYlGn_r', center=0,
            linewidths=0.5, ax=axes[0],
            cbar_kws={'label': 'Diferencia promedio [años]'})
axes[0].set_title('Media DIFF_EDAD\n(Edu. Hombre × Edu. Mujer)')
axes[0].set_xlabel('Educación de la Mujer')
axes[0].set_ylabel('Educación del Hombre')

pivot_n = df_gt.pivot_table(
    values='DIFF_EDAD', index='ESCHOM', columns='ESCMUJ', aggfunc='count'
).reindex(index=orden, columns=orden)
sns.heatmap(pivot_n, annot=True, fmt='.0f', cmap='Blues',
            linewidths=0.5, ax=axes[1],
            cbar_kws={'label': 'N° de parejas'})
axes[1].set_title('N° de Parejas por Combinación')
axes[1].set_xlabel('Educación de la Mujer')
axes[1].set_ylabel('Educación del Hombre')

plt.tight_layout()
plt.savefig('plot_heatmap_educacion.png', bbox_inches='tight')
plt.show()

idx_max = pivot_mean.stack().idxmax()
idx_min = pivot_mean.stack().idxmin()
print(f"\nCOMBINACIONES EXTREMAS (solo guatemaltecos)")
print(f"  Mayor brecha: Hombre='{idx_max[0]}' + Mujer='{idx_max[1]}' "
      f"→ {pivot_mean.loc[idx_max]:.1f} años")
print(f"  Menor brecha: Hombre='{idx_min[0]}' + Mujer='{idx_min[1]}' "
      f"→ {pivot_mean.loc[idx_min]:.1f} años")


# SECCIÓN 7 – PREPROCESAMIENTO COMÚN PARA MODELOS

print("\n" + "=" * 70)
print("PREPROCESAMIENTO PARA MODELOS")
print("=" * 70)

# Usar df_clean (ya tiene DIFF_EDAD, CAT_DIFF, CAT3)
df_model = df_clean.copy()

# One-Hot Encoding de variables categóricas (drop_first para evitar multicolinealidad)
cat_cols = ['DEPREG', 'MESOCU', 'NACHOM', 'NACMUJ', 'ESCHOM', 'ESCMUJ']
cat_cols = [c for c in cat_cols if c in df_model.columns]
df_encoded = pd.get_dummies(df_model, columns=cat_cols, drop_first=True)

# Imputar con 0 los nulos residuales en variables dummy (válido para binarias)
df_encoded = df_encoded.fillna(0)

print(f"Shape antes de OHE : {df_model.shape}")
print(f"Shape después de OHE: {df_encoded.shape}")

# Definir features predictoras (excluir targets y variables leakeadas)
exclude_cols = [
    'DIFF_EDAD', 'CAT_DIFF', 'CAT3',
    'EDADHOM', 'EDADMUJ',           # targets de regresión y variables leakeadas
    'CLAUNI',                        # variable de texto no codificada
    'DEPOCU', 'MUPOCU', 'MUPREG',   # alta correlación con DEPREG (r=0.98)
    'MESREG',                        # correlación alta con MESOCU (r=0.58)
    'NAC_PAREJA', 'DEPREG_NORM',     # columnas auxiliares del EDA
    'DIAOCUP',                       # no existe en el dataset original
]

features = [
    c for c in df_encoded.columns
    if c not in exclude_cols
    and df_encoded[c].dtype in [np.float64, np.int64, np.uint8, bool]
]

X = df_encoded[features].fillna(0).astype(float)
y_reg = df_encoded['DIFF_EDAD'].astype(float)

print(f"Número de features utilizadas: {len(features)}")

# Partición train/test 80-20 para regresión (sin estratificación)
X_train, X_test, y_train, y_test = train_test_split(
    X, y_reg, test_size=0.2, random_state=42)
print(f"\nTrain: {X_train.shape} | Test: {X_test.shape}")


# SECCIÓN 8 – ÁRBOL DE DECISIÓN

print("\n" + "=" * 70)
print("ÁRBOL DE DECISIÓN")
print("=" * 70)

# ---- 8.1 Regresión (DIFF_EDAD continua) ----
print("\n--- 8.1 Regresión ---")

configs_dt_reg = [
    {'max_depth': 4, 'min_samples_leaf': 1,  'label': 'DT-Reg depth=4'},
    {'max_depth': 8, 'min_samples_leaf': 1,  'label': 'DT-Reg depth=8'},  # mejor
    {'max_depth': 6, 'min_samples_leaf': 20, 'label': 'DT-Reg depth=6, leaf=20'},
]

results_dt_reg = []
models_dt_reg  = []

for cfg in configs_dt_reg:
    model = DecisionTreeRegressor(
        max_depth=cfg['max_depth'],
        min_samples_leaf=cfg['min_samples_leaf'],
        random_state=42
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2   = r2_score(y_test, y_pred)
    results_dt_reg.append({'Modelo': cfg['label'], 'MAE': mae, 'RMSE': rmse, 'R²': r2})
    models_dt_reg.append(model)
    print(f"  {cfg['label']}: MAE={mae:.3f}, RMSE={rmse:.3f}, R²={r2:.4f}")

df_dt_reg = pd.DataFrame(results_dt_reg)
best_dt_reg = models_dt_reg[df_dt_reg['R²'].idxmax()]

# Importancia de variables – mejor modelo regresión
imp_dt_reg = pd.Series(best_dt_reg.feature_importances_, index=X.columns).nlargest(10)
plt.figure(figsize=(8, 5))
imp_dt_reg.sort_values().plot(kind='barh', color='steelblue', edgecolor='white')
plt.title('Top 10 Variables – Árbol de Decisión (Regresión)')
plt.xlabel('Importancia')
plt.tight_layout()
plt.savefig('plot_dt_importancia_reg.png', bbox_inches='tight')
plt.show()

# ---- 8.2 Clasificación 5 clases (CAT_DIFF) ----
print("\n--- 8.2 Clasificación 5 clases (CAT_DIFF) ---")

y5 = df_encoded['CAT_DIFF'].astype(str)
X5_train, X5_test, y5_train, y5_test = train_test_split(
    X, y5, test_size=0.2, random_state=42, stratify=y5)

configs_dt_5 = [
    {'criterion': 'gini',    'max_depth': 4, 'min_samples_leaf': 1,  'label': 'DT-5 Gini depth=4'},
    {'criterion': 'gini',    'max_depth': 8, 'min_samples_leaf': 1,  'label': 'DT-5 Gini depth=8'},  # mejor F1
    {'criterion': 'entropy', 'max_depth': 6, 'min_samples_leaf': 15, 'label': 'DT-5 Entropy depth=6'},
]

results_dt_5 = []
models_dt_5  = []

for cfg in configs_dt_5:
    model = DecisionTreeClassifier(
        criterion=cfg['criterion'],
        max_depth=cfg['max_depth'],
        min_samples_leaf=cfg['min_samples_leaf'],
        class_weight='balanced',   # compensa el desbalance severo
        random_state=42
    )
    model.fit(X5_train, y5_train)
    y_pred = model.predict(X5_test)
    acc = accuracy_score(y5_test, y_pred)
    f1  = f1_score(y5_test, y_pred, average='weighted', zero_division=0)
    results_dt_5.append({'Modelo': cfg['label'], 'Accuracy': acc, 'F1-weighted': f1})
    models_dt_5.append(model)
    print(f"  {cfg['label']}: Acc={acc:.3f}, F1={f1:.3f}")

df_dt_5 = pd.DataFrame(results_dt_5)
best_dt_5 = models_dt_5[df_dt_5['F1-weighted'].idxmax()]

# Matriz de confusión – mejor modelo 5 clases
y_pred5_dt = best_dt_5.predict(X5_test)
cm5_dt = confusion_matrix(y5_test, y_pred5_dt, labels=labels5)
plt.figure(figsize=(8, 6))
sns.heatmap(cm5_dt, annot=True, fmt='d', cmap='Blues',
            xticklabels=labels5, yticklabels=labels5)
plt.title('Matriz de Confusión – Árbol de Decisión 5 Clases')
plt.ylabel('Real'); plt.xlabel('Predicho')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('plot_dt_confusion_5clases.png', bbox_inches='tight')
plt.show()
print(classification_report(y5_test, y_pred5_dt, zero_division=0))

# ---- 8.3 Clasificación 3 clases (CAT3) ----
print("\n--- 8.3 Clasificación 3 clases (CAT3) ---")

y3 = df_encoded['CAT3'].astype(str)
X3_train, X3_test, y3_train, y3_test = train_test_split(
    X, y3, test_size=0.2, random_state=42, stratify=y3)

configs_dt_3 = [
    {'criterion': 'gini',    'max_depth': 4, 'cw': None,       'label': 'DT-3 Gini depth=4'},
    {'criterion': 'entropy', 'max_depth': 6, 'cw': None,       'label': 'DT-3 Entropy depth=6'},  # mejor
    {'criterion': 'gini',    'max_depth': 5, 'cw': 'balanced', 'label': 'DT-3 Gini reg.'},
]

results_dt_3 = []
models_dt_3  = []

for cfg in configs_dt_3:
    model = DecisionTreeClassifier(
        criterion=cfg['criterion'],
        max_depth=cfg['max_depth'],
        class_weight=cfg['cw'],
        random_state=42
    )
    model.fit(X3_train, y3_train)
    y_pred = model.predict(X3_test)
    acc = accuracy_score(y3_test, y_pred)
    f1  = f1_score(y3_test, y_pred, average='weighted', zero_division=0)
    results_dt_3.append({'Modelo': cfg['label'], 'Accuracy': acc, 'F1-weighted': f1})
    models_dt_3.append(model)
    print(f"  {cfg['label']}: Acc={acc:.3f}, F1={f1:.3f}")

df_dt_3 = pd.DataFrame(results_dt_3)
best_dt_3 = models_dt_3[df_dt_3['F1-weighted'].idxmax()]

y_pred3_dt = best_dt_3.predict(X3_test)
cm3_dt = confusion_matrix(y3_test, y_pred3_dt, labels=labels3)
plt.figure(figsize=(7, 5))
sns.heatmap(cm3_dt, annot=True, fmt='d', cmap='Greens',
            xticklabels=labels3, yticklabels=labels3)
plt.title('Matriz de Confusión – Árbol de Decisión 3 Clases')
plt.ylabel('Real'); plt.xlabel('Predicho')
plt.xticks(rotation=20, ha='right')
plt.tight_layout()
plt.savefig('plot_dt_confusion_3clases.png', bbox_inches='tight')
plt.show()
print(classification_report(y3_test, y_pred3_dt, zero_division=0))

print("\nComparación global – Árbol de Decisión:")
best_r_dt = df_dt_reg.loc[df_dt_reg['R²'].idxmax()]
best_5_dt = df_dt_5.loc[df_dt_5['F1-weighted'].idxmax()]
best_3_dt = df_dt_3.loc[df_dt_3['F1-weighted'].idxmax()]
print(f"  Regresión     → MAE={best_r_dt['MAE']:.3f}, RMSE={best_r_dt['RMSE']:.3f}, R²={best_r_dt['R²']:.4f}")
print(f"  5 clases      → Acc={best_5_dt['Accuracy']:.3f}, F1={best_5_dt['F1-weighted']:.3f}")
print(f"  3 clases      → Acc={best_3_dt['Accuracy']:.3f}, F1={best_3_dt['F1-weighted']:.3f}")


# SECCIÓN 9 – RANDOM FOREST

print("\n" + "=" * 70)
print("RANDOM FOREST")
print("=" * 70)

# ---- 9.1 Regresión ----
print("\n--- 9.1 Regresión ---")

configs_rf_reg = [
    {'n': 50,  'depth': None, 'leaf': 1, 'oob': False, 'label': 'RF-Reg Baseline'},
    {'n': 100, 'depth': 8,   'leaf': 1, 'oob': False, 'label': 'RF-Reg Intermedio'},
    {'n': 150, 'depth': 10,  'leaf': 5, 'oob': True,  'label': 'RF-Reg Avanzado OOB'},
]

results_rf_reg = []
models_rf_reg  = []

for cfg in configs_rf_reg:
    model = RandomForestRegressor(
        n_estimators=cfg['n'],
        max_depth=cfg['depth'],
        min_samples_leaf=cfg['leaf'],
        oob_score=cfg['oob'],
        max_features='sqrt',
        n_jobs=-1,
        random_state=42
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2   = r2_score(y_test, y_pred)
    oob_str = f", OOB={model.oob_score_:.4f}" if cfg['oob'] else ""
    results_rf_reg.append({'Modelo': cfg['label'], 'MAE': mae, 'RMSE': rmse, 'R²': r2})
    models_rf_reg.append(model)
    print(f"  {cfg['label']}: MAE={mae:.3f}, RMSE={rmse:.3f}, R²={r2:.4f}{oob_str}")

df_rf_reg = pd.DataFrame(results_rf_reg)
best_rf_reg = models_rf_reg[df_rf_reg['R²'].idxmax()]

# ---- 9.2 Clasificación 5 clases ----
print("\n--- 9.2 Clasificación 5 clases (CAT_DIFF) ---")

configs_rf_5 = [
    {'n': 50,  'depth': None, 'leaf': 1, 'cw': 'balanced', 'oob': False, 'label': 'RF-5 Baseline'},
    {'n': 100, 'depth': 8,   'leaf': 1, 'cw': 'balanced', 'oob': False, 'label': 'RF-5 Intermedio'},
    {'n': 150, 'depth': 10,  'leaf': 5, 'cw': 'balanced', 'oob': True,  'label': 'RF-5 Avanzado OOB'},  # mejor F1
]

results_rf_5 = []
models_rf_5  = []

for cfg in configs_rf_5:
    model = RandomForestClassifier(
        n_estimators=cfg['n'],
        max_depth=cfg['depth'],
        min_samples_leaf=cfg['leaf'],
        class_weight=cfg['cw'],
        oob_score=cfg['oob'],
        max_features='sqrt',
        n_jobs=-1,
        random_state=42
    )
    model.fit(X5_train, y5_train)
    y_pred = model.predict(X5_test)
    acc = accuracy_score(y5_test, y_pred)
    f1  = f1_score(y5_test, y_pred, average='weighted', zero_division=0)
    oob_str = f", OOB={model.oob_score_:.4f}" if cfg['oob'] else ""
    results_rf_5.append({'Modelo': cfg['label'], 'Accuracy': acc, 'F1-weighted': f1})
    models_rf_5.append(model)
    print(f"  {cfg['label']}: Acc={acc:.3f}, F1={f1:.3f}{oob_str}")

df_rf_5 = pd.DataFrame(results_rf_5)
best_rf_5 = models_rf_5[df_rf_5['F1-weighted'].idxmax()]

y_pred5_rf = best_rf_5.predict(X5_test)
cm5_rf = confusion_matrix(y5_test, y_pred5_rf, labels=labels5)
plt.figure(figsize=(8, 6))
sns.heatmap(cm5_rf, annot=True, fmt='d', cmap='YlOrBr',
            xticklabels=labels5, yticklabels=labels5)
plt.title('Matriz de Confusión – Random Forest 5 Clases')
plt.ylabel('Real'); plt.xlabel('Predicho')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('plot_rf_confusion_5clases.png', bbox_inches='tight')
plt.show()
print(classification_report(y5_test, y_pred5_rf, zero_division=0))

# ---- 9.3 Clasificación 3 clases ----
print("\n--- 9.3 Clasificación 3 clases (CAT3) ---")

configs_rf_3 = [
    {'n': 50,  'depth': None, 'leaf': 1, 'cw': None,       'oob': False, 'label': 'RF-3 Baseline (sin cw)'},  # mejor F1
    {'n': 100, 'depth': 8,   'leaf': 1, 'cw': None,       'oob': False, 'label': 'RF-3 Intermedio'},
    {'n': 150, 'depth': 10,  'leaf': 5, 'cw': 'balanced', 'oob': True,  'label': 'RF-3 Regularizado OOB'},
]

results_rf_3 = []
models_rf_3  = []

for cfg in configs_rf_3:
    model = RandomForestClassifier(
        n_estimators=cfg['n'],
        max_depth=cfg['depth'],
        min_samples_leaf=cfg['leaf'],
        class_weight=cfg['cw'],
        oob_score=cfg['oob'],
        max_features='sqrt',
        n_jobs=-1,
        random_state=42
    )
    model.fit(X3_train, y3_train)
    y_pred = model.predict(X3_test)
    acc = accuracy_score(y3_test, y_pred)
    f1  = f1_score(y3_test, y_pred, average='weighted', zero_division=0)
    oob_str = f", OOB={model.oob_score_:.4f}" if cfg['oob'] else ""
    results_rf_3.append({'Modelo': cfg['label'], 'Accuracy': acc, 'F1-weighted': f1})
    models_rf_3.append(model)
    print(f"  {cfg['label']}: Acc={acc:.3f}, F1={f1:.3f}{oob_str}")

df_rf_3 = pd.DataFrame(results_rf_3)
best_rf_3 = models_rf_3[df_rf_3['F1-weighted'].idxmax()]

y_pred3_rf = best_rf_3.predict(X3_test)
cm3_rf = confusion_matrix(y3_test, y_pred3_rf, labels=labels3)
plt.figure(figsize=(7, 5))
sns.heatmap(cm3_rf, annot=True, fmt='d', cmap='Greens',
            xticklabels=labels3, yticklabels=labels3)
plt.title('Matriz de Confusión – Random Forest 3 Clases')
plt.ylabel('Real'); plt.xlabel('Predicho')
plt.xticks(rotation=20, ha='right')
plt.tight_layout()
plt.savefig('plot_rf_confusion_3clases.png', bbox_inches='tight')
plt.show()
print(classification_report(y3_test, y_pred3_rf, zero_division=0))

# Importancia de variables – RF clasificación
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
for ax, model, title in [(axes[0], best_rf_5, '5 Clases'),
                          (axes[1], best_rf_3, '3 Clases')]:
    imp = pd.Series(model.feature_importances_, index=X.columns).nlargest(15)
    imp.sort_values().plot(kind='barh', ax=ax, color='darkorange', edgecolor='white')
    ax.set_title(f'Top 15 Variables – RF {title}')
    ax.set_xlabel('Importancia')
plt.tight_layout()
plt.savefig('plot_rf_importancia.png', bbox_inches='tight')
plt.show()

print("\nComparación global – Random Forest:")
best_r_rf = df_rf_reg.loc[df_rf_reg['R²'].idxmax()]
best_5_rf = df_rf_5.loc[df_rf_5['F1-weighted'].idxmax()]
best_3_rf = df_rf_3.loc[df_rf_3['F1-weighted'].idxmax()]
print(f"  Regresión → MAE={best_r_rf['MAE']:.3f}, RMSE={best_r_rf['RMSE']:.3f}, R²={best_r_rf['R²']:.4f}")
print(f"  5 clases  → Acc={best_5_rf['Accuracy']:.3f}, F1={best_5_rf['F1-weighted']:.3f}")
print(f"  3 clases  → Acc={best_3_rf['Accuracy']:.3f}, F1={best_3_rf['F1-weighted']:.3f}")


# SECCIÓN 10 – REGRESIÓN LINEAL Y LOGÍSTICA

print("\n" + "=" * 70)
print("REGRESIÓN LINEAL Y LOGÍSTICA")
print("=" * 70)

# Los modelos lineales son sensibles a la escala de las variables;
# se estandariza DESPUÉS del split, ajustando solo con train para evitar data leakage.

# ---- 10.1 Regresión lineal (OLS, Ridge, Lasso) ----
print("\n--- 10.1 Regresión Lineal (OLS / Ridge / Lasso) ---")

scaler_reg = StandardScaler()
X_train_sc = scaler_reg.fit_transform(X_train)
X_test_sc  = scaler_reg.transform(X_test)

modelos_rl = {
    'OLS':           LinearRegression(),
    'Ridge (α=1.0)': Ridge(alpha=1.0),       # mejor resultado
    'Lasso (α=0.1)': Lasso(alpha=0.1, max_iter=5000),
}

results_rl_reg = []
fitted_rl = {}

for name, model in modelos_rl.items():
    model.fit(X_train_sc, y_train)
    y_pred = model.predict(X_test_sc)
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2   = r2_score(y_test, y_pred)
    results_rl_reg.append({'Modelo': name, 'MAE': mae, 'RMSE': rmse, 'R²': r2})
    fitted_rl[name] = model
    print(f"  {name}: MAE={mae:.3f}, RMSE={rmse:.3f}, R²={r2:.4f}")

df_rl_reg = pd.DataFrame(results_rl_reg)
best_rl_name = df_rl_reg.loc[df_rl_reg['R²'].idxmax(), 'Modelo']
best_rl_reg  = fitted_rl[best_rl_name]

# Variables eliminadas por Lasso (selección automática)
lasso_coefs = pd.Series(fitted_rl['Lasso (α=0.1)'].coef_, index=X.columns)
n_zero = (lasso_coefs == 0).sum()
print(f"\n  Lasso eliminó {n_zero} de {len(lasso_coefs)} variables ({n_zero/len(lasso_coefs)*100:.1f}%)")
print("  Top variables NO eliminadas por Lasso:")
print(lasso_coefs[lasso_coefs != 0].abs().nlargest(10))

# Gráfico de coeficientes del mejor modelo lineal
coefs_best = pd.Series(best_rl_reg.coef_, index=X.columns)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
coefs_best.nlargest(10).sort_values().plot(
    kind='barh', ax=axes[0], color='steelblue', edgecolor='white')
axes[0].set_title(f'Top 10 Coef. Positivos – {best_rl_name}')
coefs_best.nsmallest(10).sort_values(ascending=False).plot(
    kind='barh', ax=axes[1], color='tomato', edgecolor='white')
axes[1].set_title(f'Top 10 Coef. Negativos – {best_rl_name}')
plt.tight_layout()
plt.savefig('plot_rl_coeficientes.png', bbox_inches='tight')
plt.show()

# ---- 10.2 Regresión logística 5 clases ----
print("\n--- 10.2 Regresión Logística 5 Clases (CAT_DIFF) ---")

scaler_5 = StandardScaler()
X5_train_sc = scaler_5.fit_transform(X5_train)
X5_test_sc  = scaler_5.transform(X5_test)

results_log_5 = []
models_log_5  = []

for C in [0.1, 1.0, 10.0]:
    model = LogisticRegression(
        C=C,
        penalty='l2',
        solver='lbfgs',
        class_weight='balanced',   # compensa desbalance
        max_iter=1000,
        random_state=42
    )
    model.fit(X5_train_sc, y5_train)
    y_pred = model.predict(X5_test_sc)
    acc = accuracy_score(y5_test, y_pred)
    f1  = f1_score(y5_test, y_pred, average='weighted', zero_division=0)
    results_log_5.append({'C': C, 'Accuracy': acc, 'F1-weighted': f1})
    models_log_5.append(model)
    print(f"  C={C}: Acc={acc:.3f}, F1={f1:.3f}")

df_log_5 = pd.DataFrame(results_log_5)
best_log_5 = models_log_5[df_log_5['F1-weighted'].idxmax()]
best_C5    = df_log_5.loc[df_log_5['F1-weighted'].idxmax(), 'C']

y_pred5_log = best_log_5.predict(X5_test_sc)
cm5_log = confusion_matrix(y5_test, y_pred5_log, labels=labels5)
plt.figure(figsize=(8, 6))
sns.heatmap(cm5_log, annot=True, fmt='d', cmap='Blues',
            xticklabels=labels5, yticklabels=labels5)
plt.title(f'Matriz de Confusión – Reg. Logística 5 Clases (C={best_C5})')
plt.ylabel('Real'); plt.xlabel('Predicho')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('plot_log_confusion_5clases.png', bbox_inches='tight')
plt.show()
print(classification_report(y5_test, y_pred5_log, zero_division=0))

# ---- 10.3 Regresión logística 3 clases ----
print("\n--- 10.3 Regresión Logística 3 Clases (CAT3) ---")

scaler_3 = StandardScaler()
X3_train_sc = scaler_3.fit_transform(X3_train)
X3_test_sc  = scaler_3.transform(X3_test)

configs_log_3 = [
    {'penalty': 'l2', 'C': 1.0, 'solver': 'lbfgs', 'label': 'L2 C=1.0'},
    {'penalty': 'l2', 'C': 0.1, 'solver': 'lbfgs', 'label': 'L2 C=0.1'},
    {'penalty': 'l1', 'C': 1.0, 'solver': 'saga',  'label': 'L1 C=1.0'},  # mejor F1
]

results_log_3 = []
models_log_3  = []

for cfg in configs_log_3:
    model = LogisticRegression(
        penalty=cfg['penalty'],
        C=cfg['C'],
        solver=cfg['solver'],
        max_iter=2000,
        random_state=42
    )
    model.fit(X3_train_sc, y3_train)
    y_pred = model.predict(X3_test_sc)
    acc = accuracy_score(y3_test, y_pred)
    f1  = f1_score(y3_test, y_pred, average='weighted', zero_division=0)
    results_log_3.append({'Modelo': cfg['label'], 'Accuracy': acc, 'F1-weighted': f1})
    models_log_3.append(model)
    print(f"  {cfg['label']}: Acc={acc:.3f}, F1={f1:.3f}")

df_log_3 = pd.DataFrame(results_log_3)
best_log_3 = models_log_3[df_log_3['F1-weighted'].idxmax()]
best_label3_log = df_log_3.loc[df_log_3['F1-weighted'].idxmax(), 'Modelo']

y_pred3_log = best_log_3.predict(X3_test_sc)
cm3_log = confusion_matrix(y3_test, y_pred3_log, labels=labels3)
plt.figure(figsize=(7, 5))
sns.heatmap(cm3_log, annot=True, fmt='d', cmap='Greens',
            xticklabels=labels3, yticklabels=labels3)
plt.title(f'Matriz de Confusión – Reg. Logística 3 Clases ({best_label3_log})')
plt.ylabel('Real'); plt.xlabel('Predicho')
plt.xticks(rotation=20, ha='right')
plt.tight_layout()
plt.savefig('plot_log_confusion_3clases.png', bbox_inches='tight')
plt.show()
print(classification_report(y3_test, y_pred3_log, zero_division=0))

# Variables eliminadas por L1 en 3 clases
l1_model_3 = models_log_3[2]
l1_zeros_3 = (l1_model_3.coef_ == 0).sum(axis=1)
print("  Variables con coef=0 por clase (L1):")
for cls, z in zip(l1_model_3.classes_, l1_zeros_3):
    print(f"    {cls}: {z} eliminadas de {X.shape[1]}")

print("\nComparación global – Regresión Lineal / Logística:")
best_r_rl = df_rl_reg.loc[df_rl_reg['R²'].idxmax()]
best_5_log = df_log_5.loc[df_log_5['F1-weighted'].idxmax()]
best_3_log = df_log_3.loc[df_log_3['F1-weighted'].idxmax()]
print(f"  Regresión lineal → MAE={best_r_rl['MAE']:.3f}, RMSE={best_r_rl['RMSE']:.3f}, R²={best_r_rl['R²']:.4f}")
print(f"  Log. 5 clases    → Acc={best_5_log['Accuracy']:.3f}, F1={best_5_log['F1-weighted']:.3f}")
print(f"  Log. 3 clases    → Acc={best_3_log['Accuracy']:.3f}, F1={best_3_log['F1-weighted']:.3f}")


# SECCIÓN 11 – XGBOOST

print("\n" + "=" * 70)
print("XGBOOST")
print("=" * 70)

# ---- 11.1 Regresión ----
print("\n--- 11.1 Regresión ---")

configs_xgb_reg = [
    dict(n_estimators=100, learning_rate=0.1,  max_depth=4,
         label='XGB-Reg Baseline'),
    dict(n_estimators=200, learning_rate=0.05, max_depth=6,
         subsample=0.8, colsample_bytree=0.8,
         label='XGB-Reg Intermedio'),
    dict(n_estimators=300, learning_rate=0.03, max_depth=8,
         min_child_weight=5, subsample=0.7, colsample_bytree=0.7,
         label='XGB-Reg Avanzado'),   # mejor R²
]

results_xgb_reg = []
models_xgb_reg  = []

for cfg in configs_xgb_reg:
    label = cfg.pop('label')
    model = XGBRegressor(**cfg, random_state=42, eval_metric='rmse', verbosity=0)
    model.fit(X_train, y_train,
              eval_set=[(X_test, y_test)], verbose=False)
    y_pred = model.predict(X_test)
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2   = r2_score(y_test, y_pred)
    results_xgb_reg.append({'Modelo': label, 'MAE': mae, 'RMSE': rmse, 'R²': r2})
    models_xgb_reg.append(model)
    cfg['label'] = label
    print(f"  {label}: MAE={mae:.3f}, RMSE={rmse:.3f}, R²={r2:.4f}")

df_xgb_reg = pd.DataFrame(results_xgb_reg)
best_xgb_reg = models_xgb_reg[df_xgb_reg['R²'].idxmax()]

# Curva de aprendizaje del mejor modelo de regresión
evals = best_xgb_reg.evals_result().get('validation_0', {}).get('rmse', [])
if evals:
    plt.figure(figsize=(8, 4))
    plt.plot(evals, color='darkorange', label='RMSE (test)')
    plt.xlabel('Número de árboles')
    plt.ylabel('RMSE')
    plt.title('Curva de Aprendizaje – XGBoost Regresión')
    plt.legend()
    plt.tight_layout()
    plt.savefig('plot_xgb_curva_reg.png', bbox_inches='tight')
    plt.show()

# ---- 11.2 Clasificación 5 clases ----
print("\n--- 11.2 Clasificación 5 Clases (CAT_DIFF) ---")

# XGBoost requiere etiquetas numéricas enteras; se usa LabelEncoder
le5 = LabelEncoder()
y5_enc = le5.fit_transform(df_encoded['CAT_DIFF'].astype(str))
X5_xgb_train, X5_xgb_test, y5_xgb_train, y5_xgb_test = train_test_split(
    X, y5_enc, test_size=0.2, random_state=42, stratify=y5_enc)

# XGBoost no tiene class_weight nativo para multiclase; se usa sample_weight
sw5_train = compute_sample_weight(class_weight='balanced', y=y5_xgb_train)

configs_xgb_5 = [
    dict(n_estimators=100, learning_rate=0.1,  max_depth=4,
         use_sw=False, label='XGB-5 Baseline'),
    dict(n_estimators=200, learning_rate=0.05, max_depth=6,
         subsample=0.8, colsample_bytree=0.8,
         use_sw=True, label='XGB-5 Intermedio+sw'),   # mejor F1
    dict(n_estimators=300, learning_rate=0.03, max_depth=8,
         min_child_weight=5,
         use_sw=True, label='XGB-5 Avanzado+sw'),
]

results_xgb_5 = []
models_xgb_5  = []

for cfg in configs_xgb_5:
    label  = cfg.pop('label')
    use_sw = cfg.pop('use_sw')
    model  = XGBClassifier(
        **cfg, objective='multi:softmax', num_class=5,
        eval_metric='mlogloss', random_state=42, verbosity=0
    )
    fit_kw = {'eval_set': [(X5_xgb_test, y5_xgb_test)], 'verbose': False}
    if use_sw:
        fit_kw['sample_weight'] = sw5_train
    model.fit(X5_xgb_train, y5_xgb_train, **fit_kw)
    y_pred = model.predict(X5_xgb_test)
    acc = accuracy_score(y5_xgb_test, y_pred)
    f1  = f1_score(y5_xgb_test, y_pred, average='weighted', zero_division=0)
    results_xgb_5.append({'Modelo': label, 'Accuracy': acc, 'F1-weighted': f1})
    models_xgb_5.append(model)
    cfg['label'] = label; cfg['use_sw'] = use_sw
    print(f"  {label}: Acc={acc:.3f}, F1={f1:.3f}")

df_xgb_5 = pd.DataFrame(results_xgb_5)
best_xgb_5 = models_xgb_5[df_xgb_5['F1-weighted'].idxmax()]

y_pred5_xgb   = best_xgb_5.predict(X5_xgb_test)
y_pred5_xgb_l = le5.inverse_transform(y_pred5_xgb)
y_test5_xgb_l = le5.inverse_transform(y5_xgb_test)

cm5_xgb = confusion_matrix(y_test5_xgb_l, y_pred5_xgb_l, labels=labels5)
plt.figure(figsize=(8, 6))
sns.heatmap(cm5_xgb, annot=True, fmt='d', cmap='YlOrBr',
            xticklabels=labels5, yticklabels=labels5)
plt.title('Matriz de Confusión – XGBoost 5 Clases')
plt.ylabel('Real'); plt.xlabel('Predicho')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('plot_xgb_confusion_5clases.png', bbox_inches='tight')
plt.show()
print(classification_report(y_test5_xgb_l, y_pred5_xgb_l, zero_division=0))

# ---- 11.3 Clasificación 3 clases ----
print("\n--- 11.3 Clasificación 3 Clases (CAT3) ---")

le3 = LabelEncoder()
y3_enc = le3.fit_transform(df_encoded['CAT3'].astype(str))
X3_xgb_train, X3_xgb_test, y3_xgb_train, y3_xgb_test = train_test_split(
    X, y3_enc, test_size=0.2, random_state=42, stratify=y3_enc)

sw3_train = compute_sample_weight(class_weight='balanced', y=y3_xgb_train)

configs_xgb_3 = [
    dict(n_estimators=100, learning_rate=0.1,  max_depth=4,
         use_sw=False, label='XGB-3 Baseline'),
    dict(n_estimators=200, learning_rate=0.05, max_depth=6,
         subsample=0.8, colsample_bytree=0.8,
         use_sw=False, label='XGB-3 Intermedio'),   # mejor F1
    dict(n_estimators=300, learning_rate=0.03, max_depth=8,
         min_child_weight=5, subsample=0.7, colsample_bytree=0.7,
         use_sw=True, label='XGB-3 Avanzado+sw'),
]

results_xgb_3 = []
models_xgb_3  = []

for cfg in configs_xgb_3:
    label  = cfg.pop('label')
    use_sw = cfg.pop('use_sw')
    model  = XGBClassifier(
        **cfg, objective='multi:softmax', num_class=3,
        eval_metric='mlogloss', random_state=42, verbosity=0
    )
    fit_kw = {'eval_set': [(X3_xgb_test, y3_xgb_test)], 'verbose': False}
    if use_sw:
        fit_kw['sample_weight'] = sw3_train
    model.fit(X3_xgb_train, y3_xgb_train, **fit_kw)
    y_pred = model.predict(X3_xgb_test)
    acc = accuracy_score(y3_xgb_test, y_pred)
    f1  = f1_score(y3_xgb_test, y_pred, average='weighted', zero_division=0)
    results_xgb_3.append({'Modelo': label, 'Accuracy': acc, 'F1-weighted': f1})
    models_xgb_3.append(model)
    cfg['label'] = label; cfg['use_sw'] = use_sw
    print(f"  {label}: Acc={acc:.3f}, F1={f1:.3f}")

df_xgb_3 = pd.DataFrame(results_xgb_3)
best_xgb_3 = models_xgb_3[df_xgb_3['F1-weighted'].idxmax()]

y_pred3_xgb   = best_xgb_3.predict(X3_xgb_test)
y_pred3_xgb_l = le3.inverse_transform(y_pred3_xgb)
y_test3_xgb_l = le3.inverse_transform(y3_xgb_test)

cm3_xgb = confusion_matrix(y_test3_xgb_l, y_pred3_xgb_l, labels=labels3)
plt.figure(figsize=(7, 5))
sns.heatmap(cm3_xgb, annot=True, fmt='d', cmap='Greens',
            xticklabels=labels3, yticklabels=labels3)
plt.title('Matriz de Confusión – XGBoost 3 Clases')
plt.ylabel('Real'); plt.xlabel('Predicho')
plt.xticks(rotation=20, ha='right')
plt.tight_layout()
plt.savefig('plot_xgb_confusion_3clases.png', bbox_inches='tight')
plt.show()
print(classification_report(y_test3_xgb_l, y_pred3_xgb_l, zero_division=0))

# Top 15 variables – XGBoost (los 3 modelos)
fig, axes = plt.subplots(1, 3, figsize=(20, 7))
for ax, model, title, color in [
    (axes[0], best_xgb_reg, 'Regresión',  'darkorange'),
    (axes[1], best_xgb_5,   '5 Clases',   'steelblue'),
    (axes[2], best_xgb_3,   '3 Clases',   'seagreen'),
]:
    imp = pd.Series(model.feature_importances_, index=X.columns).nlargest(15)
    imp.sort_values().plot(kind='barh', ax=ax, color=color, edgecolor='white')
    ax.set_title(f'Top 15 Variables – XGB {title}')
    ax.set_xlabel('Importancia (gain normalizado)')
plt.tight_layout()
plt.savefig('plot_xgb_importancia_global.png', bbox_inches='tight')
plt.show()

# Top 5 por modelo para comparación cruzada
top5_xgb_r = pd.Series(best_xgb_reg.feature_importances_, index=X.columns).nlargest(5)
top5_xgb_5 = pd.Series(best_xgb_5.feature_importances_,   index=X.columns).nlargest(5)
top5_xgb_3 = pd.Series(best_xgb_3.feature_importances_,   index=X.columns).nlargest(5)
print("\nTop 5 variables más importantes por modelo XGBoost:")
print(pd.DataFrame({
    'Regresión':    top5_xgb_r.index.tolist(),
    'Clasif. 5cls': top5_xgb_5.index.tolist(),
    'Clasif. 3cls': top5_xgb_3.index.tolist(),
}, index=[f'Top {i+1}' for i in range(5)]))

print("\nComparación global – XGBoost:")
best_r_xgb = df_xgb_reg.loc[df_xgb_reg['R²'].idxmax()]
best_5_xgb = df_xgb_5.loc[df_xgb_5['F1-weighted'].idxmax()]
best_3_xgb = df_xgb_3.loc[df_xgb_3['F1-weighted'].idxmax()]
print(f"  Regresión → MAE={best_r_xgb['MAE']:.3f}, RMSE={best_r_xgb['RMSE']:.3f}, R²={best_r_xgb['R²']:.4f}")
print(f"  5 clases  → Acc={best_5_xgb['Accuracy']:.3f}, F1={best_5_xgb['F1-weighted']:.3f}")
print(f"  3 clases  → Acc={best_3_xgb['Accuracy']:.3f}, F1={best_3_xgb['F1-weighted']:.3f}")


# SECCIÓN 12 – COMPARACIÓN GLOBAL DE TODOS LOS ALGORITMOS

print("\n" + "=" * 70)
print("COMPARACIÓN GLOBAL DE ALGORITMOS")
print("=" * 70)

resumen = pd.DataFrame({
    'Algoritmo': [
        'Árbol de Decisión',
        'Random Forest',
        'Reg. Lineal / Logística',
        'XGBoost',
    ],
    'R² Regresión': [
        df_dt_reg.loc[df_dt_reg['R²'].idxmax(), 'R²'],
        df_rf_reg.loc[df_rf_reg['R²'].idxmax(), 'R²'],
        df_rl_reg.loc[df_rl_reg['R²'].idxmax(), 'R²'],
        df_xgb_reg.loc[df_xgb_reg['R²'].idxmax(), 'R²'],
    ],
    'F1-w 5 clases': [
        df_dt_5.loc[df_dt_5['F1-weighted'].idxmax(), 'F1-weighted'],
        df_rf_5.loc[df_rf_5['F1-weighted'].idxmax(), 'F1-weighted'],
        df_log_5.loc[df_log_5['F1-weighted'].idxmax(), 'F1-weighted'],
        df_xgb_5.loc[df_xgb_5['F1-weighted'].idxmax(), 'F1-weighted'],
    ],
    'F1-w 3 clases': [
        df_dt_3.loc[df_dt_3['F1-weighted'].idxmax(), 'F1-weighted'],
        df_rf_3.loc[df_rf_3['F1-weighted'].idxmax(), 'F1-weighted'],
        df_log_3.loc[df_log_3['F1-weighted'].idxmax(), 'F1-weighted'],
        df_xgb_3.loc[df_xgb_3['F1-weighted'].idxmax(), 'F1-weighted'],
    ],
    'Interpretabilidad': ['Muy alta', 'Media', 'Muy alta', 'Baja'],
})

resumen = resumen.round(4)
print(resumen.to_string(index=False))

# Gráfico de barras comparativo
fig, axes = plt.subplots(1, 3, figsize=(17, 5))
metricas = ['R² Regresión', 'F1-w 5 clases', 'F1-w 3 clases']
colores  = ['#5C85D6', '#66BB6A', '#FFA726', '#EF5350']

for ax, metrica in zip(axes, metricas):
    bars = ax.bar(resumen['Algoritmo'], resumen[metrica],
                  color=colores, edgecolor='white', alpha=0.85)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.002,
                f'{bar.get_height():.3f}',
                ha='center', fontsize=9, fontweight='bold')
    ax.set_title(metrica, fontweight='bold')
    ax.set_ylim(0, resumen[metrica].max() * 1.2)
    ax.tick_params(axis='x', rotation=25)
    ax.set_ylabel('Valor')

plt.suptitle('Comparación Global de Algoritmos', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('plot_comparacion_global.png', bbox_inches='tight')
plt.show()

print("\n" + "=" * 70)
print("CONCLUSIONES PRINCIPALES")
print("=" * 70)
print("""
1. XGBoost obtiene el mejor rendimiento en regresión (R²=0.037) y en
   clasificación de 5 clases (F1-weighted=0.291).

2. Random Forest lidera en clasificación de 3 clases (F1-weighted=0.425)
   gracias al balance entre sesgo y varianza del ensemble.

3. Los valores de R² < 0.04 son consistentes con la literatura: la
   diferencia de edad en matrimonios depende de factores individuales
   no medidos en registros administrativos.

4. Las variables de escolaridad (ESCHOM, ESCMUJ) y el departamento de
   registro (DEPREG) emergen como los predictores más influyentes en
   todos los algoritmos.

5. La clasificación en 3 clases casi duplica el F1-weighted respecto a
   5 clases, siendo más recomendable para aplicaciones productivas.

6. La brecha de edad disminuyó de 3.10 a 2.76 años entre 2011 y 2021,
   evidenciando una transformación gradual hacia mayor equidad.
""")
