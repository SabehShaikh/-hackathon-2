-- Database Schema for Todo AI Chatbot - Phase 3
-- Target: Neon PostgreSQL (shared with Phase 2)
-- Migration: Alembic-managed (see data-model.md)

-- =============================================================================
-- PHASE 2 TABLES (EXISTING - NO CHANGES)
-- =============================================================================

-- Users table (Phase 2 - DO NOT MODIFY)
-- Already exists from Phase 2 deployment
-- CREATE TABLE users (
--     id VARCHAR(255) PRIMARY KEY,
--     email VARCHAR(255) UNIQUE NOT NULL,
--     password_hash VARCHAR(255) NOT NULL,
--     created_at TIMESTAMP DEFAULT NOW()
-- );
-- CREATE INDEX idx_users_email ON users(email);

-- Tasks table (Phase 2 - DO NOT MODIFY)
-- Already exists from Phase 2 deployment
-- CREATE TABLE tasks (
--     id SERIAL PRIMARY KEY,
--     user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
--     title VARCHAR(500) NOT NULL,
--     description TEXT,
--     completed BOOLEAN DEFAULT FALSE,
--     created_at TIMESTAMP DEFAULT NOW(),
--     updated_at TIMESTAMP DEFAULT NOW()
-- );
-- CREATE INDEX idx_tasks_user_id ON tasks(user_id);
-- CREATE INDEX idx_tasks_completed ON tasks(completed);

-- =============================================================================
-- PHASE 3 TABLES (NEW - MIGRATION REQUIRED)
-- =============================================================================

-- Conversations table
-- Stores chat sessions between user and AI agent
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes for conversations
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_conversations_updated_at ON conversations(updated_at DESC);

-- Messages table
-- Stores individual messages in conversations (user + assistant)
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes for messages
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);

-- =============================================================================
-- COMMENTS (DOCUMENTATION)
-- =============================================================================

COMMENT ON TABLE conversations IS 'Chat sessions between users and AI agent. Persists conversation context for multi-session continuity.';
COMMENT ON COLUMN conversations.user_id IS 'Foreign key to users table. One user can have multiple conversations.';
COMMENT ON COLUMN conversations.created_at IS 'Timestamp when conversation started.';
COMMENT ON COLUMN conversations.updated_at IS 'Timestamp of last message in conversation. Updated by application layer.';

COMMENT ON TABLE messages IS 'Individual messages in conversations. Stores both user inputs and AI responses.';
COMMENT ON COLUMN messages.conversation_id IS 'Foreign key to conversations table. Messages belong to exactly one conversation.';
COMMENT ON COLUMN messages.user_id IS 'Foreign key to users table. For verification that message belongs to conversation owner.';
COMMENT ON COLUMN messages.role IS 'Message sender: "user" for user inputs, "assistant" for AI responses.';
COMMENT ON COLUMN messages.content IS 'Message text content. Max 10,000 characters (validated in application layer).';
COMMENT ON COLUMN messages.created_at IS 'Timestamp when message was created. Used for chronological ordering.';

-- =============================================================================
-- DATA INTEGRITY CHECKS
-- =============================================================================

-- Verify foreign key constraints
DO $$
BEGIN
    -- Check conversations.user_id references users.id
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints
        WHERE constraint_type = 'FOREIGN KEY'
        AND table_name = 'conversations'
        AND constraint_name LIKE '%user_id%'
    ) THEN
        RAISE EXCEPTION 'Missing foreign key: conversations.user_id -> users.id';
    END IF;

    -- Check messages.conversation_id references conversations.id
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints
        WHERE constraint_type = 'FOREIGN KEY'
        AND table_name = 'messages'
        AND constraint_name LIKE '%conversation_id%'
    ) THEN
        RAISE EXCEPTION 'Missing foreign key: messages.conversation_id -> conversations.id';
    END IF;

    -- Check messages.user_id references users.id
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints
        WHERE constraint_type = 'FOREIGN KEY'
        AND table_name = 'messages'
        AND constraint_name LIKE '%user_id%'
    ) THEN
        RAISE EXCEPTION 'Missing foreign key: messages.user_id -> users.id';
    END IF;

    RAISE NOTICE 'All foreign key constraints verified successfully';
END $$;

-- =============================================================================
-- SAMPLE QUERIES (FOR TESTING)
-- =============================================================================

-- Get user's latest conversation
-- SELECT * FROM conversations
-- WHERE user_id = 'user123'
-- ORDER BY updated_at DESC
-- LIMIT 1;

-- Load conversation history (chronological order)
-- SELECT role, content, created_at
-- FROM messages
-- WHERE conversation_id = 1
-- ORDER BY created_at ASC;

-- Count messages in conversation
-- SELECT COUNT(*) FROM messages
-- WHERE conversation_id = 1;

-- Get user's conversations with message counts
-- SELECT
--     c.id,
--     c.created_at,
--     c.updated_at,
--     COUNT(m.id) as message_count
-- FROM conversations c
-- LEFT JOIN messages m ON c.id = m.conversation_id
-- WHERE c.user_id = 'user123'
-- GROUP BY c.id
-- ORDER BY c.updated_at DESC;

-- =============================================================================
-- ROLLBACK SCRIPT (FOR MIGRATION DOWNGRADE)
-- =============================================================================

-- To rollback Phase 3 tables (CAUTION: DELETES ALL CONVERSATION DATA)
-- DROP INDEX IF EXISTS idx_messages_created_at;
-- DROP INDEX IF EXISTS idx_messages_user_id;
-- DROP INDEX IF EXISTS idx_messages_conversation_id;
-- DROP TABLE IF EXISTS messages;
--
-- DROP INDEX IF EXISTS idx_conversations_updated_at;
-- DROP INDEX IF EXISTS idx_conversations_created_at;
-- DROP INDEX IF EXISTS idx_conversations_user_id;
-- DROP TABLE IF EXISTS conversations;

-- =============================================================================
-- MIGRATION NOTES
-- =============================================================================

-- This script is for reference only.
-- Actual migrations managed via Alembic (see backend/migrations/).
--
-- To apply migrations:
--   cd backend/
--   alembic upgrade head
--
-- To rollback migrations:
--   alembic downgrade -1
--
-- To check current version:
--   alembic current
--
-- IMPORTANT:
-- - Phase 2 tables (users, tasks) are NOT modified
-- - Phase 3 tables reference Phase 2 tables via foreign keys
-- - Foreign keys use ON DELETE CASCADE for cleanup
-- - All indexes created for optimal query performance
-- - No data loss for Phase 2 on rollback (Phase 3 tables only)
