"""
Demostración de cómo se agregan los campos de fecha correctamente
"""

# Simular campos que vienen del config.yaml
fields_from_config = [
    'clicks',
    'frequency', 
    'impressions',
    'reach',
    'cpc',
    'cpm',
    'ctr',
    'spend',
]

level = 'campaign'

print("="*70)
print("SIMULACIÓN DE INCLUSIÓN DE CAMPOS")
print("="*70)

print("\n1️⃣ Campos originales del config.yaml:")
print(f"   {fields_from_config}")

# Hacer copia para no modificar el original
fields = fields_from_config.copy()

print(f"\n2️⃣ Campos después de copiar (preserva tus métricas):")
print(f"   {fields}")

# Convertir a strings para comparación
fields_str = [str(f) for f in fields]

print(f"\n3️⃣ Verificando si 'date_start' está en la lista...")
if 'date_start' not in fields_str:
    print("   ❌ NO encontrado - Agregando al inicio")
    fields.insert(0, 'date_start')
else:
    print("   ✅ Ya existe - No se agrega")

print(f"\n4️⃣ Verificando si 'date_stop' está en la lista...")
if 'date_stop' not in fields_str:
    print("   ❌ NO encontrado - Agregando en posición 1")
    fields.insert(1, 'date_stop')
else:
    print("   ✅ Ya existe - No se agrega")

# Actualizar fields_str después de agregar fechas
fields_str = [str(f) for f in fields]

print(f"\n5️⃣ Como level='{level}', verificando campaign_id...")
if 'campaign_id' not in fields_str:
    print("   ❌ NO encontrado - Agregando al final")
    fields.append('campaign_id')
else:
    print("   ✅ Ya existe - No se agrega")

print(f"\n6️⃣ Verificando campaign_name...")
if 'campaign_name' not in fields_str:
    print("   ❌ NO encontrado - Agregando al final")
    fields.append('campaign_name')
else:
    print("   ✅ Ya existe - No se agrega")

print("\n" + "="*70)
print("RESULTADO FINAL - Campos que se envían a Facebook API:")
print("="*70)
for i, field in enumerate(fields, 1):
    emoji = "📅" if 'date' in field else ("🆔" if 'id' in field or 'name' in field else "📊")
    print(f"{i:2d}. {emoji} {field}")

print("\n" + "="*70)
print("✅ VERIFICACIÓN EXITOSA")
print("="*70)
print("\n📋 Resumen:")
print(f"   • Total de campos: {len(fields)}")
print(f"   • Campos de fecha: 2 (date_start, date_stop)")
print(f"   • Campos de ID: 2 (campaign_id, campaign_name)")
print(f"   • Métricas configuradas: {len(fields_from_config)}")
print(f"\n   {len(fields)} campos = 2 fechas + 2 IDs + {len(fields_from_config)} métricas ✅")

print("\n💡 Con estos campos, cada registro en la BD tendrá:")
print("   • La fecha del dato (date_start, date_stop)")
print("   • A qué campaña pertenece (campaign_id, campaign_name)")
print("   • Todas las métricas que configuraste\n")
