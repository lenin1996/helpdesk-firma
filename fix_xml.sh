#!/bin/bash
# Script para limpiar espacios o contenido antes de <?xml ... ?> en todos los XML de un módulo Odoo

# Recorrer todos los XML
find . -name "*.xml" | while read -r f; do
    # Hacer backup por seguridad
    cp "$f" "$f.bak"

    # Eliminar cualquier línea antes de <?xml ... ?>
    awk 'BEGIN{found=0} 
         /^<\?xml/{found=1} 
         {if(found) print}' "$f.bak" > "$f"

    echo "Procesado: $f (backup en $f.bak)"
done

echo "✅ Todos los archivos XML han sido limpiados."
