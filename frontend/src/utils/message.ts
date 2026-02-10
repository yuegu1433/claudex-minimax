import { detectFileType } from './fileTypes';
import type { Message } from '@/types';
import { generateUUID } from './uuid';

export function createInitialMessage(
  prompt: string,
  attachedFiles: File[] | null,
  modelId: string,
  chatId: string,
): Message {
  return {
    id: generateUUID(),
    chat_id: chatId,
    content: prompt,
    role: 'user',
    is_bot: false,
    attachments:
      attachedFiles && attachedFiles.length > 0
        ? attachedFiles.map((file) => {
            const fileUrl = URL.createObjectURL(file);
            return {
              id: generateUUID(),
              message_id: generateUUID(),
              file_url: fileUrl,
              file_type: detectFileType(file.name, file.type),
              filename: file.name,
              created_at: new Date().toISOString(),
            };
          })
        : undefined,
    created_at: new Date().toISOString(),
    model_id: modelId,
  };
}

export function createAttachmentsFromFiles(
  files: File[] | null,
  storeBlobUrl: (file: File, url: string) => void,
) {
  if (!files || files.length === 0) return undefined;

  return files.map((file) => {
    const fileType = detectFileType(file.name, file.type);
    const blobUrl = URL.createObjectURL(file);

    if (fileType === 'pdf') {
      storeBlobUrl(file, blobUrl);
    }

    return {
      id: generateUUID(),
      message_id: Date.now().toString(),
      file_url: blobUrl,
      file_type: fileType,
      filename: file.name,
      created_at: new Date().toISOString(),
    };
  });
}

export const findLastBotMessageIndex = (messages: Message[]): number => {
  for (let i = messages.length - 1; i >= 0; i--) {
    if (messages[i].is_bot) {
      return i;
    }
  }
  return -1;
};
