import { Hono } from 'hono'
import { serve } from '@hono/node-server'
import { writeFile, mkdir } from 'fs/promises'
import path from 'path'

const app = new Hono()

app.get('/', (c) => {
  return c.text('Hello Hono!')
})

app.post('/upload', async (c) => {
  try {
    const body = await c.req.parseBody()
    const file = body['image'] as File

    if (!file) {
      return c.text('No se recibió ninguna imagen', 400)
    }

    const arrayBuffer = await file.arrayBuffer()
    const buffer = Buffer.from(arrayBuffer)

    const uploadDir = path.join(process.cwd(), 'imagenes')
    await mkdir(uploadDir, { recursive: true })

    const filePath = path.join(uploadDir, file.name)

    await writeFile(filePath, buffer)

    return c.json({
      message: 'Imagen guardada correctamente',
      file: file.name,
    })

  } catch (error) {
    console.error(error)
    return c.text('Error al subir la imagen', 500)
  }
})

serve({
  fetch: app.fetch,
  port: 3001
}, (info) => {
  console.log(`Server is running on http://localhost:${info.port}`)
})
